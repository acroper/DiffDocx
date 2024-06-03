# DiffDocx
Utility for applying diff on a docx document

**Current State:**
Working for test files.
Requires utilities such as diff, cmp, and xxd, commonly pre-installed on most Linux distros.



**Usage:**

To generate diff:

python3 /diffdocx_path/diffdocx.py -diff file1.docx file2.docx diff.patch

To patch a file:

python3 /diffdocx_path/diffdocx.py -patch file1.docx diff.patch restored.docx


