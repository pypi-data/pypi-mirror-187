import torch
from torch import nn
from PIL import Image
from typing import Optional

from .swinir import SwinIR, swin_ir_inference
from .bsrgan import RRDBNet, bsrgan_inference
from .realesrgan import patch_realesrgan_param_names

from sldl._utils import get_checkpoint_path


class ImageSR(nn.Module):
    r"""Image Super-Resolution

    Takes an image and increases its resoulution by some factor. Currently supports
    SwinIR, BSRGAN and RealESRGAN models.

    :param model_name: Name of the pre-trained model. Can be one of the `SwinIR-M`,
        `SwinIR-L`, `BSRGAN`, `BSRGANx2`, and `RealESRGAN`. Default: `SwinIR-M`.
    :type model_name: str
    :param precision:  Can be either `full` (uses fp32) and `half` (uses fp16).
        Default: `full`.
    :type precision: str

    Example:

    .. code-block:: python

        from PIL import Image
        from sldl.image import ImageSR

        sr = ImageSR('BSRGAN')
        img = Image.open('test.png')
        upscaled = sr(img)
    """

    def __init__(self, model_name: str = "SwinIR-M", precision: str = "full"):
        super(ImageSR, self).__init__()
        self.model_name = model_name
        self.precision = precision
        if model_name in ["SwinIR-M", "SwinIR-L"]:
            if model_name == "SwinIR-M":
                self.model = SwinIR(
                    upscale=4,
                    in_chans=3,
                    img_size=64,
                    window_size=8,
                    img_range=1.0,
                    depths=[6, 6, 6, 6, 6, 6],
                    embed_dim=180,
                    num_heads=[6, 6, 6, 6, 6, 6],
                    mlp_ratio=2,
                    upsampler="nearest+conv",
                    resi_connection="1conv",
                )
                path = get_checkpoint_path(
                    "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth"
                )
                pretrained_model = torch.load(path)
            else:
                self.model = SwinIR(
                    upscale=4,
                    in_chans=3,
                    img_size=64,
                    window_size=8,
                    img_range=1.0,
                    depths=[6, 6, 6, 6, 6, 6, 6, 6, 6],
                    embed_dim=240,
                    num_heads=[8, 8, 8, 8, 8, 8, 8, 8, 8],
                    mlp_ratio=2,
                    upsampler="nearest+conv",
                    resi_connection="3conv",
                )
                path = get_checkpoint_path(
                    "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth"
                )
                pretrained_model = torch.load(path)
            self.model.load_state_dict(
                pretrained_model["params_ema"]
                if "params_ema" in pretrained_model.keys()
                else pretrained_model,
                strict=True,
            )
        elif model_name in ["BSRGAN", "BSRGANx2"]:
            self.model = RRDBNet(
                in_nc=3,
                out_nc=3,
                nf=64,
                nb=23,
                gc=32,
                sf=2 if model_name == "BSRGANx2" else 4,
            )
            path = get_checkpoint_path(
                f"https://github.com/cszn/KAIR/releases/download/v1.0/{model_name}.pth"
            )
            self.model.load_state_dict(torch.load(path), strict=True)
        elif model_name == "RealESRGAN":
            self.model = RRDBNet(
                in_nc=3,
                out_nc=3,
                nf=64,
                nb=23,
                gc=32,
                sf=4
            )
            path = get_checkpoint_path(
                "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
            )
            self.model.load_state_dict(patch_realesrgan_param_names(torch.load(path)), strict=True)
        else:
            raise ValueError("Unknown model name")

        if precision == "half":
            self.model = self.model.half()

    @property
    def device(self) -> torch.device:
        return next(self.parameters()).device

    def __call__(self, img: Image.Image, device: Optional[torch.device] = None) -> Image.Image:
        """Applies the model.

        :param img: An input image.
        :type img: :class:`PIL.Image.Image`

        :return: An upscaled version of the input image
        :rtype: :class:`PIL.Image.Image`
        """
        device = device if device is not None else self.device
        if self.model_name in ["SwinIR-M", "SwinIR-L"]:
            return swin_ir_inference(
                self.model, img, device=device, precision=self.precision
            )
        elif self.model_name in ["BSRGAN", "BSRGANx2", "RealESRGAN"]:
            return bsrgan_inference(
                self.model, img, device=device, precision=self.precision
            )
