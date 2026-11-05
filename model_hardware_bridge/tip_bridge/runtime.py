"""Keep the upstream annotation guard without inspect.stack() source lookups."""
import dataclasses,functools,inspect,sys
from typing import get_args,get_origin


def fast_annotation_check(original,compiler=None):
    def check(instance,typechecker):
        frame=sys._getframe(1)
        try:
            while frame is not None:
                if frame.f_globals.get('__name__') in {'jax._src.tree_util','flax.nnx.transforms.compilation'}:
                    return None
                frame=frame.f_back
        finally:
            del frame
        if compiler is None:return original(instance,typechecker)
        fields=[];values={}
        for field in dataclasses.fields(instance):
            annotation=field.type
            if isinstance(annotation,str):continue
            args=get_args(annotation)
            if get_origin(annotation) is type and len(args)==1 and isinstance(args[0],str):continue
            try:values[field.name]=getattr(instance,field.name)
            except AttributeError:continue
            fields.append(field)
        return compiler(type(instance),typechecker,tuple(fields))(instance,**values)
    return check


@functools.lru_cache(maxsize=128)
def compiled_check(cls,typechecker,fields):
    import jaxtyping._decorator as decorator
    parameters=[inspect.Parameter('self',inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    parameters.extend(inspect.Parameter(f.name,inspect.Parameter.POSITIONAL_OR_KEYWORD,annotation=f.type) for f in fields)
    function=decorator._make_fn_with_signature(cls.__name__,cls.__qualname__,cls.__module__,inspect.Signature(parameters),output=False)
    return decorator.jaxtyped(function,typechecker=typechecker)


def install_annotation_check():
    import jaxtyping._decorator
    from openpi.shared import array_typing
    jaxtyping._decorator._check_dataclass_annotations=fast_annotation_check(array_typing._original_check_dataclass_annotations,compiled_check)
