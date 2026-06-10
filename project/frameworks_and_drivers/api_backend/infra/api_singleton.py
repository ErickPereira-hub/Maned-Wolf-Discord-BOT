from .api_config import KernelApi
from .routes import routes

KERNEL_API: KernelApi = KernelApi(routes)