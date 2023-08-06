# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logbesselk', 'logbesselk.jax', 'logbesselk.tensorflow']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logbesselk',
    'version': '3.2.0',
    'description': 'Provide function to calculate the modified Bessel function of the second kind',
    'long_description': '# logbesselk\nProvide function to calculate the modified Bessel function of the second kind\nand its derivatives.\n\n## Reference\nTakashi Takekawa, Fast parallel calculation of modified Bessel function\nof the second kind and its derivatives, SoftwareX, 17, 100923, 2022.\n\n## Author\nTAKEKAWA Takashi <takekawa@tk2lab.org>\n\n\n## For Tensorflow\n\n### Require\n- Python (>=3.8)\n- Tensorflow (>=2.6)\n\n### Installation\n```shell\npip install tensorflow logbesselk\n```\n\n### Examples\n```python\nimport tensorflow as tf\nfrom logbesselk.tensorflow import log_bessel_k as logk\nfrom logbesselk.jax import bessel_ke as ke\nfrom logbesselk.jax import bessel_kratio as kratio\n\nv = 1.0\nx = 1.0\na = logk(v, x)\n\nv = jnp.linspace(1, 10, 10)\nx = jnp.linspace(1, 10, 10)\nb = logk(v, x)\n\n# gradient\nwith tf.GradientTape() as g:\n    g.watch(v, x)\n    f = logk(v, x)\ndlogkdv = g.gradient(f, v)\ndlogkdx = g.gradient(f, x)\n\n# use tf.function\nlogk = tf.function(logk)\n\n# advanced version\nfrom logbesselk.tensorflow import log_abs_deriv_bessel_k\n\nlogk = lambda v, x: log_abs_deriv_bessel_k(v, x, 0, 0)\nlogdkdv = lambda v, x: log_abs_deriv_bessel_k(v, x, 1, 0)\nlogdkdx = lambda v, x: log_abs_deriv_bessel_k(v, x, 0, 1)\n```\n\n\n## For jax\n\n### Require\n- Python (>=3.8)\n- jax (>=0.3)\n\n### Installation\n```shell\npip install jax[cuda] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html\npip install logbesselk\n```\n\n### Examples\n```python\nimport jax\nimport jax.numpy as jnp\nfrom logbesselk.jax import log_bessel_k as logk\nfrom logbesselk.jax import bessel_ke as ke\nfrom logbesselk.jax import bessel_kratio as kratio\n\n# scalar func and grad\nv = 1.0\nx = 1.0\na = logk(v, x)\n\n# dlogK/dv = (dK/dv) / K\ndlogkdv = jax.grad(logk, 0)\nb = dlogkdv(v, x)\n\n# dlogK/dx = (dK/dx) / K\ndlogkdx = jax.grad(logk, 1)\nc = dlogkdx(v, x)\n\n# misc\nd = ke(v, x)\ne = kratio(v, x, d=1)\n\n# vectorize\nlogk_vec = jax.vmap(logk)\n\nv = jnp.linspace(1, 10, 10)\nx = jnp.linspace(1, 10, 10)\nf = logk_vec(v)\n\n# use jit\nlogk_vec_jit = jax.jit(logk_vec)\n\n# advanced version\nfrom logbesselk.jax import log_abs_devel_bessel_k\n\nlog_dkdv = lambda v, x: log_abs_deriv_bessel_k(v, x, 1, 0)\nlog_dkdx = lambda v, x: log_abs_deriv_bessel_k(v, x, 0, 1)\n\nlog_dkdv_jit = jax.jit(jax.vmap(log_dkdv))\nlog_dkdx_jit = jax.jit(jax.vmap(log_dkdx))\n```\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tk2lab/logbesselk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
