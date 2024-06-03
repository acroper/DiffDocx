#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DiffDocx
Copyright (C) 2024  Jorge Guerrero - acroper@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import shutil
import xml.etree.ElementTree as ET
import tempfile
import subprocess
import zipfile

from indexfile import *

def diffiles(input1, input2, patchfile):
    # First, create a temporal folders
    
    DocLocation =  tempfile.mkdtemp(prefix= "diffDoc" )
    # DocLocation = "/tmp/DocX"
    
    origPath = DocLocation+"/original"
    modPath = DocLocation+"/modified"
    diffPath = DocLocation+"/diff"
    
    # Extract the files
    
    with zipfile.ZipFile(input1, 'r') as zip_ref:
      zip_ref.extractall(origPath)
    
    
    with zipfile.ZipFile(input2, 'r') as zip_ref:
      zip_ref.extractall(modPath)
    
    
    
    current_working_directory = os.getcwd()
    
    
    # Generate a file list of input2
    
    index = indexfile()
    
    print("Checking files...")
    
    index.searchFiles(modPath, origPath, diffPath, DocLocation)
    
    index.createDiff(patchfile)  # Collect the binary parts/changes of the file
    
    os.chdir(DocLocation)  

    subprocess.call("diff -ruN original/ modified/ > diff/diff.patch ", shell=True)   
    
    os.chdir(diffPath)
    # zip the diff folder
    
    subprocess.call("zip -r ../diff.zip * ", shell=True) 
    
    os.chdir(current_working_directory) 
    
    shutil.copy(os.path.join(DocLocation, "diff.zip"), patchfile)  
    
    # Delete the temporal folders
    shutil.rmtree(DocLocation)
    


def patchfiles(input1, patchfile, output1):
    # Create temporal folders
    DocLocation =  tempfile.mkdtemp(prefix= "diffDoc" )
    # DocLocation = "/tmp/DocX2"
    
    origPath = DocLocation+"/original"
    modPath = DocLocation+"/modified"
    diffPath = DocLocation+"/diff"
    
    
    # Extract the files
    
    with zipfile.ZipFile(input1, 'r') as zip_ref:
      zip_ref.extractall(origPath)

    with zipfile.ZipFile(patchfile, 'r') as zip_ref:
      zip_ref.extractall(origPath)      
    
    current_working_directory = os.getcwd()
    
    
    shutil.move(os.path.join(origPath, "diff.patch"  ), os.path.join(DocLocation, "diff.patch"))
    
    os.chdir(DocLocation)  
    
    subprocess.call("patch -s -p0 < diff.patch ", shell=True)    
    # Extract the files
    
    os.chdir(origPath)
    
    subprocess.call("zip -r ../restored.docx * ", shell=True)   
    
    # outputfile = os.path.join(current_working_directory, output1)
    
    os.chdir(current_working_directory)
    
    shutil.copy(os.path.join(DocLocation, "restored.docx"), output1)
    
    
    # Delete temporal files
    shutil.rmtree(DocLocation)
    
    
    
    
    
    


def main():
    args = sys.argv[1:]
    
    Passed = False
    
    if len(args) == 4 and args[0] == "-diff":
        print("Applying diff")
        diffiles(args[1], args[2], args[3])
        Passed = True
        
    if len(args) == 4 and args[0] == "-patch":
        print("Applying patch")
        patchfiles(args[1], args[2], args[3])
        Passed = True
        
    if Passed == False:
        print("Invalid arguments")
        print("Usage: ")
        print("diffdocx.py -diff file1.docx file2.docx diffdoc.patch: Diff files and save in diffdoc.patch")
        print("diffdocx.py -patch file3.docx diffdoc.patch file4.docx: Patches file3.docx using diffdoc.patch")
    
    
    
    
    

if __name__ == "__main__":
    
    
#     # Test files

    Testing = False   #Enable to test without using command line
    
    if Testing:
        current_working_directory = os.getcwd()
        
        file1 = os.path.join(current_working_directory, "test/file1.docx")
        file2 = os.path.join(current_working_directory, "test/file2.docx")
        restored = os.path.join(current_working_directory, "test/restored.docx")
        patchfile = os.path.join(current_working_directory, "test/diff.patch")
        
        
        test = "diff"  
        # test = "patch"   # Uncomment to test patching file
        
        
        if test == "diff":
            sys.argv=["","-diff",file1, file2, patchfile]
            
        if test == "patch":
            sys.argv=["","-patch",file1, patchfile, restored]
    
    
    main( )