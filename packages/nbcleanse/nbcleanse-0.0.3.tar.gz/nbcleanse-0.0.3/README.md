# nbcleanse 🚿
A notebook cleaner to end all notebook cleaners

## What?

It's a script that cleans [notebooks](https://jupyter.org/) of "redundant components" like metadata/output and etc.

## Why?

Because notebooks ARE code and whatever goes into your codebase should be as lean as possible.  
Many IDEs which implement a notebook inteface (VScode, Jetbrains and etc.) add data to notebooks files in order to provide some functionalities. And that's a problem:  

**It makes code reviews more difficult**  
Notebook outputs clutter file data. Even with services such as reviewNB which allow simpler code reviews on notebook, cell outputs create a lot of false positive code changes.  

**It is not consistant across IDEs**  
Different IDEs can override the same settings causign unexpected behaviour.  

**It is not consistant across developers**  
The added settings can contain assumptions about dependencies that are computer-specific (conda environment, package versions). This can create conflicts when others pull the repo.

## Why nbcleanse?

Because it's lightweight, configureable and let's you know how many lines of code you've saved your repo - thus making you happy.  

## OK. How?

First Install:
```bash
pip install nbcleanse
```
Then run:
```bash
cd your/notebooks/dir/
nbcleanse
```

## Can it do this or that?

It might! Currently supported features are:

```bash
# cleans all metadata from all notebooks in cwd
nbcleanse -m

# cleans all outputs
nbcleanse -o

# cleans all cell execution counts
nbcleanse -e

# quiet mode
nbcleanse -q

# flags are additive
nbcleanse -moeq
```

## It'd be nice if it could do this or the other thing...

Any suggesstions are welcome. Please open an issue or a PR explaining your idea!  
