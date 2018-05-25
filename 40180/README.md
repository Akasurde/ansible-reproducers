Typecasting Long value using Python3 and Pyvmomi
================================================

In Python 3, `int` and `long` is merged. So setting Long values using Python 3 using Pyvmomi raises error with native datatypes.

But we can use Pyvmomi datatypes to typecast `int` into `long`

Use - 

```
option_manager = host.configManager.advancedOption
option = vim.option.OptionValue()
option.key = 'UserVars.ESXiShellInteractiveTimeOut'
option.value = VmomiSupport.vmodlTypes['long'](12) # Use Pyvmomi native datatype for long
option_manager.UpdateOptions(changedValue=[option])
```
