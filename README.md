EvoGFuzz
=======

This repo contains EvoGFuzz and other tools for comparison.

# How to run EvoGFuzz?

In general, you got to /evogfuzz and you call something like

```
python3 evogfuzz.py --output <out_dir> --target <subject_driver>
```

where
* `<output_dir>` is where evogfuzz's output shows up
* `<subject_driver>` is a python file which contains a ``execute_samples()`` method,
  which returns the driver object for the program under test.

The ``subject_driver`` for existing subjects can be found in the subfolders of the subjects/ folder.
If you e.g. want to run Rhino you would invoke

```
python3 evogfuzz.py --output ../results --target ../subjects/Rhino/subject_driver.py
```

# How to add subjects?

* `<grammar_driver>` ..
* `<subject_driver>` ..

# Requirements

In order to run EvoGFuzzm, the ANTLR parser generator (Version 4.7.1) is required.
Additionally, the class path for antlr4 needs to be exported.

```
export CLASSPATH=".:/<path-to-ANTLR-library>/antlr-4.5-complete.jar:$CLASSPATH"
java org.antlr.v4.Tool
```