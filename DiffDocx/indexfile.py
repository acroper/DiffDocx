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

import os
import xml.etree.ElementTree as ET
import difflib
import subprocess
import shutil

class indexfile:
    
    def __init__(self):
        
        
        self.RootFolder = folder()
        
    
    def searchFiles (self, modified, original, diffPath, docloc):
        # Search files in the modified folder, and looks for their changes
        
        self.RootFolder.OriPath = original
        self.RootFolder.ModPath = modified
        self.RootFolder.DiffPath = diffPath
        
        self.RootFolder.DocLocation = docloc
        
        os.makedirs(self.RootFolder.DiffPath, exist_ok=True)
        
        os.makedirs(os.path.join(self.RootFolder.DocLocation, "tmp"), exist_ok=True)
        
        self.diffFile = os.path.join(diffPath, "patchfile.patch")
        
        self.RootFolder.searchFiles()
        
    def createDiff(self, patchfile):
        
        # subprocess.call("diff -ruN "+self.RootFolder.OriPath+"  "+self.RootFolder.ModPath + " > " + patchfile , shell=True)
        print("Search changes in the binary subfiles")
        self.RootFolder.createDiff()
        
        
        
        
                
                

class folder:

    def __init__(self):
        
        self.OriPath = ""
        self.ModPath = ""
        self.DiffPath = ""
        
        self.DocLocation = ""
        
        self.ListFiles = []
        self.ListFolders = []
        
    def checkFolder(self):
        
        # if os.path.exists(self.OriPath):
        #     print(self.OriPath + " Exists")
        # else:
        #     print(self.OriPath + " Does not exist")
            
        os.makedirs(self.DiffPath, exist_ok=True)
            
    def createDiff(self):
        for nfolder in self.ListFolders:
            nfolder.createDiff()
        
        for nfile in self.ListFiles:
            nfile.createDiff()
        
    
    def searchFiles (self):
        # Search files in the modified folder, and looks for their changes
        
        obj = os.scandir(self.ModPath)
        
        for entry in obj:
            if entry.is_dir():
                
                nfolder = folder()
                nfolder.OriPath = os.path.join( self.OriPath, entry.name)
                nfolder.ModPath = os.path.join( self.ModPath, entry.name)
                nfolder.DiffPath = os.path.join( self.DiffPath, entry.name)
                nfolder.DocLocation = self.DocLocation
                
                self.ListFolders.append(nfolder)
                
                nfolder.checkFolder()
                
                nfolder.searchFiles()
                
            else:
                
                nfile = filed()
                nfile.OriPath = os.path.join( self.OriPath, entry.name)
                nfile.ModPath = os.path.join( self.ModPath, entry.name)
                nfile.DiffPath = os.path.join( self.DiffPath, entry.name)
                nfile.DocLocation = self.DocLocation
                
                self.ListFiles.append(nfile)
                nfile.CheckFile()
                

class filed:
    def __init__(self):
        
        self.OriPath = ""
        self.ModPath = ""
        self.DiffPath = ""
        self.DocLocation = ""
        
        self.diff = ""
        
        self.action = "None"
        
    def CheckFile(self):
        
        if os.path.exists(self.OriPath):
            print(self.OriPath + " Exists")
        else:
            print(self.OriPath + " Does not exist")
            
    def createDiff(self):
        
        self.action = "None"
        
        Ori = os.path.exists(self.OriPath)
        
        Mod = os.path.exists(self.ModPath)
        
        
        if not Ori and Mod:
            self.action = "Replace"
        
        if Ori and not Mod:
            self.action = "Remove"
        
        if Ori and Mod and not ( ".xml" in self.OriPath ) :
            self.action = "Verify"
            
            # copy original al modified
            tmpfolder = os.path.join(self.DocLocation, "tmp")
            A_file = os.path.join(tmpfolder, "A")
            B_file = os.path.join(tmpfolder, "B")
            patchfile = os.path.join(tmpfolder, "patch.txt")
            
            shutil.copy(self.OriPath, A_file + ".bin" )
            shutil.copy(self.ModPath, B_file + ".bin" )
            
            current_working_directory = os.getcwd()
            
            os.chdir(tmpfolder)
            # convert to hex
            subprocess.call("xxd A.bin > A.hex ", shell=True)
            subprocess.call("xxd B.bin > B.hex ", shell=True)
            subprocess.call("diff A.hex B.hex > patch.txt", shell=True)
            
            # verifying the size of the patch
            size = os.stat("patch.txt").st_size
            
            os.chdir(current_working_directory)
            
            if size != 0:
                self.action = "Replace"
            else:
                self.action = "Ignore"
                
                
        
        
        if self.action == "Replace":
            # copy the file to the patch folder
            shutil.copy(self.ModPath, self.DiffPath)
            print("Replacing binary part")
        
        
        
        
        
    
        
        
        
    