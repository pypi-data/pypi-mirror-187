"""
@author: Bishal Thapaliya
@email: bthapaliya16@gmail.com
"""

from os import sep as _sep
import torch as _torch
import os as _os
from coinstac_sparse_dinunet import config as _conf
from coinstac_sparse_dinunet.utils import tensorutils as _tu
import numpy as _np
import coinstac_sparse_dinunet.utils as _utils


class COINNLearner:
    def __init__(self, trainer=None, mp_pool=None, **kw):
        self.cache = trainer.cache
        self.input = trainer.input
        self.state = trainer.state
        self.trainer = trainer
        self.global_modes = self.input.get('global_modes', {})
        self.pool = mp_pool
        self.dtype = f"float{self.cache['precision_bits']}"
        self.device = trainer.device["gpu"]
        self.cache['log_dir'] = _os.path.join(
            self.state['outputDirectory'],
            self.cache['task_id'],
            f"fold_0"
        )
        self.my_logger = open(self.cache['log_dir'] + _os.sep + f"locallogs.json", 'a')


    
    def get_model_sps(self, model):
        nonzero = total = 0
        for name, param in model.named_parameters():
            if 'mask' not in name:
                tensor = param.detach().clone()
                # nz_count.append(torch.count_nonzero(tensor))
                nz_count = _torch.count_nonzero(tensor).item()
                total_params = tensor.numel()
                nonzero += nz_count
                total += total_params
        
        tensor = None
        # print(f"TOTAL: {total}")
        abs_sps = 100 * (total-nonzero) / total
        return abs_sps


    def step(self) -> dict:
        out = {}
        grads = _tu.load_arrays_learner(self.state['baseDirectory'] + _sep + self.input['avg_grads_file'])
        grad_index = 0
        first_model = list(self.trainer.nn.keys())[0]

        for i, param in enumerate(self.trainer.nn[first_model].named_parameters()):
            if 'mask' not in param[0]:
                param[1].grad = _torch.tensor(grads[grad_index], dtype=_torch.float32).to(self.device)
                grad_index += 1

        first_optim = list(self.trainer.optimizer.keys())[0]
        self.trainer.optimizer[first_optim].step()
        return out

    def backward(self):
        out = {}
        first_model = list(self.trainer.nn.keys())[0]
        first_optim = list(self.trainer.optimizer.keys())[0]

        self.trainer.nn[first_model].train()
        self.trainer.optimizer[first_optim].zero_grad()
        its = []
        for _ in range(self.cache['local_iterations']):
            batch, nxt_iter_out = self.trainer.data_handle.next_iter()
            it = self.trainer.iteration(batch)
            it['loss'].backward()
            its.append(it)
            out.update(**nxt_iter_out)
        return self.trainer.reduce_iteration(its), out

    # def to_reduce(self):
    #     it, out = self.backward()
    #     first_model = list(self.trainer.nn.keys())[0]
    #     out['grads_file'] = _conf.grads_file
    #     grads = _tu.extract_grads(self.trainer.nn[first_model], dtype=self.dtype)
    #     _tu.save_arrays(
    #         self.state['transferDirectory'] + _sep + out['grads_file'],
    #         _np.array(grads, dtype=object)
    #     )
    #     out['reduce'] = True
    #     return it, out

    def to_reduce(self):
        it, out = self.backward()
        first_model = list(self.trainer.nn.keys())[0]
        out['grads_file'] = _conf.grads_file
        grads = _tu.extract_grads(self.trainer.nn[first_model], dtype=self.dtype)
        model_sparsity = self.get_model_sps(self.trainer.nn[first_model])
        self.my_logger.write("\n The model sparsity before transferring is  " + str(model_sparsity))
        finalgrads = []
        for param_grads in grads:
            non_zero_grad_indices = _np.array(_np.nonzero(param_grads))
            values_nonzero = param_grads[_np.nonzero(param_grads)]
            sps_grads = _torch.sparse_coo_tensor(non_zero_grad_indices, values_nonzero)
            finalgrads.append(sps_grads)


        _tu.save_arrays(
            self.state['transferDirectory'] + _sep + out['grads_file'],
            finalgrads
        )
        out['reduce'] = True
        return it, out

