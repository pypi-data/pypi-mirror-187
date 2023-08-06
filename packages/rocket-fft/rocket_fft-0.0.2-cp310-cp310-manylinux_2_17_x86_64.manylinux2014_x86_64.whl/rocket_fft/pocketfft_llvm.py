from functools import partial

from llvmlite import ir
from numba.core import types
from numba.core.cgutils import get_or_insert_function
from numba.extending import intrinsic

# ll_array_as_voidptr is used in template string
from .pocketfft_utils import ll_array_as_voidptr, load_pocketfft

ll_size_t = ir.IntType(64)
ll_int64 = ir.IntType(64)
ll_double = ir.DoubleType()
ll_bool = ir.IntType(1)
ll_voidptr = ir.IntType(8).as_pointer()
ll_void = ir.VoidType()

void = types.void
size_t = types.size_t


def _partial(func, *args, **kargs):
    func = func.__func__
    return partial(func, *args, **kargs)


class Pocketfft:
    def __init__(self):
        self.dll = load_pocketfft()

    @staticmethod
    def _call_cmplx(fname, builder, args):
        fntype = ir.FunctionType(
            ll_void,
            (
                ll_size_t,  # ndim
                ll_voidptr,  # ain
                ll_voidptr,  # aout
                ll_voidptr,  # axes
                ll_bool,  # forward
                ll_double,  # fct
                ll_size_t,  # nthreads
            )
        )
        fn = get_or_insert_function(builder.module, fntype, fname)
        return builder.call(fn, args)

    c2c = _partial(_call_cmplx, "numba_c2c")
    r2c = _partial(_call_cmplx, "numba_r2c")
    c2r = _partial(_call_cmplx, "numba_c2r")
    c2c_sym = _partial(_call_cmplx, "numba_c2c_sym")

    @staticmethod
    def _call_real(fname, builder, args):
        fntype = ir.FunctionType(
            ll_void,
            (
                ll_size_t,  # ndim
                ll_voidptr,  # ain
                ll_voidptr,  # aout
                ll_voidptr,  # axes
                ll_int64,  # type
                ll_double,  # fct
                ll_bool,  # ortho
                ll_size_t,  # nthreads
            )
        )
        fn = get_or_insert_function(builder.module, fntype, fname)
        return builder.call(fn, args)

    dct = _partial(_call_real, "numba_dct")
    dst = _partial(_call_real, "numba_dst")

    @staticmethod
    def _call_hartley(fname, builder, args):
        fntype = ir.FunctionType(
            ll_void,
            (
                ll_size_t,  # ndim
                ll_voidptr,  # ain
                ll_voidptr,  # aout
                ll_voidptr,  # axes
                ll_double,  # fct
                ll_size_t,  # nthreads
            )
        )
        fn = get_or_insert_function(builder.module, fntype, fname)
        return builder.call(fn, args)

    separable_hartley = _partial(_call_hartley, "numba_separable_hartley")
    genuine_hartley = _partial(_call_hartley, "numba_genuine_hartley")

    @staticmethod
    def fftpack(builder, args):
        fname = "numba_fftpack"
        fntype = ir.FunctionType(
            ll_void,
            (
                ll_size_t,  # ndim
                ll_voidptr,  # ain
                ll_voidptr,  # aout
                ll_voidptr,  # axes
                ll_bool,  # real2hermitian
                ll_bool,  # forward
                ll_double,  # fct
                ll_size_t,  # nthreads
            )
        )
        fn = get_or_insert_function(builder.module, fntype, fname)
        return builder.call(fn, args)

    @staticmethod
    def good_size(builder, args):
        fname = "numba_good_size"
        fntype = ir.FunctionType(
            ll_size_t,
            (
                ll_size_t,  # target
                ll_bool,  # real
            )
        )
        fn = get_or_insert_function(builder.module, fntype, fname)
        return builder.call(fn, args)


pocketfft = Pocketfft()


_tmpl = """
def _(typingctx, ain, aout, axes, {0}):
    def codegen(context, builder, sig, args):
        ain, aout, axes, *rest = args
        ain_t, aout_t, axes_t, *_ = sig.args

        ndim = ll_size_t(ain_t.ndim)
        ain_ptr = ll_array_as_voidptr(context, builder, ain_t, ain)
        aout_ptr = ll_array_as_voidptr(context, builder, aout_t, aout)
        ax_ptr = ll_array_as_voidptr(context, builder, axes_t, axes)

        args = (ndim, ain_ptr, aout_ptr, ax_ptr, *rest)
        pocketfft.{1}(builder, args)
        
    sig = void(ain, aout, axes, {0})
    return sig, codegen
"""


class Builder:
    def __init__(self, *extra_args):
        self.extra_args = ", ".join(extra_args)

    def __call__(self, fname):
        src = _tmpl.format(self.extra_args, fname)
        exec(src)
        func = locals()["_"]
        func.__name__ = fname
        return intrinsic(func)


cmplx_builder = Builder("forward", "fct", "nthreads")
numba_c2c = cmplx_builder("c2c")
numba_r2c = cmplx_builder("r2c")
numba_c2r = cmplx_builder("c2r")
numba_c2c_sym = cmplx_builder("c2c_sym")

real_builder = Builder("type", "fct", "ortho", "nthreads")
numba_dst = real_builder("dst")
numba_dct = real_builder("dct")

hartley_builder = Builder("fct", "nthreads")
numba_separable_hartley = hartley_builder("separable_hartley")
numba_genuine_hartley = hartley_builder("genuine_hartley")

fftpack_builder = Builder("real2hermitian", "forward", "fct", "nthreads")
numba_fftpack = fftpack_builder("fftpack")


@intrinsic
def numba_good_size(typingctx, n, real):
    def codegen(context, builder, sig, args):
        ret = pocketfft.good_size(builder, args)
        return ret

    sig = size_t(n, real)
    return sig, codegen
