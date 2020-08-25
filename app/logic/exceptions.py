from gwpycore import GruntWurkError, GruntWurkConfigError, GruntWurkConfigSettingWarning, GruntWurkArgumentError

class RadioLogError(GruntWurkError):
    pass

class RadioLogArgumentError(GruntWurkArgumentError):
    pass

class RadioLogConfigError(GruntWurkConfigError):
    pass

class RadioLogConfigSettingWarning(GruntWurkConfigSettingWarning):
    pass

__all__ = ("RadioLogError", "RadioLogArgumentError", "RadioLogConfigError", "RadioLogConfigSettingWarning")
