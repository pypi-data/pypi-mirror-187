import sten
import torch
import copy


class FixedMaskTensor:
    def __init__(self, val, mask, n, m, g):
        assert torch.all(
            torch.isclose(mask, torch.zeros_like(mask))
            | torch.isclose(mask, torch.ones_like(mask))
        )
        self.val = val
        self.mask = mask

    @staticmethod
    def from_dense(tensor, n, m, g):
        mask = torch.where(
            tensor.abs() < 1e-6,
            torch.zeros_like(tensor, dtype=torch.bool),
            torch.ones_like(tensor, dtype=torch.bool),
        )
        return FixedMaskTensor(tensor * mask, mask, n, m, g)

    def to_dense(self):
        return copy.deepcopy(self.val)

    def numel(self):
        return self.val.numel()

    def to(self, device=None, dtype=None, non_blocking=False, copy=False):
        return FixedMaskTensor(
            self.val.to(device=device, dtype=dtype, copy=True),
            self.mask.to(device=device, dtype=dtype, copy=True),
            self.n,
            self.m,
            self.g,
        )

    @property
    def shape(self):
        return self.val.shape

    @property
    def device(self):
        return self.val.device

    @property
    def dtype(self):
        return self.val.dtype