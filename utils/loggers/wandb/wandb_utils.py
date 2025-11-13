"""Minimal WandbLogger shim for environments without W&B or missing local module.
This provides a no-op logger that implements the interface expected by utils.loggers.Loggers.
It avoids failing imports if wandb isn't installed. If wandb is installed, this shim will still
work but won't attempt to call remote APIs.
"""

from types import SimpleNamespace

class WandbLogger:
    def __init__(self, opt, run_id=None):
        # Minimal attributes used elsewhere in code
        self.opt = opt
        self.run_id = run_id
        self.data_dict = None
        # simulate a wandb_run object with .summary and .id
        self.wandb_run = SimpleNamespace(id=(run_id or 'local_run'), summary={})
        self.current_epoch = 0

    def log(self, data: dict, step: int = None):
        # no-op: keep log local or print if needed
        return

    def val_one_image(self, pred, predn, path, names, im):
        # no-op
        return

    def log_model(self, model_dir, opt, epoch, fi, best_model=False):
        # no-op
        return

    def finish_run(self):
        # no-op
        return

    def end_epoch(self, best_result=False):
        # no-op
        return

    def __getattr__(self, item):
        # Provide safe defaults for any other attribute access
        return lambda *a, **k: None
