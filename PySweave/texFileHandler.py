# -------------------------------------------------------------------
# - NAME:        texFileHandler.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2017-09-25
# -------------------------------------------------------------------
# - DESCRIPTION:
# -------------------------------------------------------------------
# - EDITORIAL:   2017-09-25, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2017-10-06 09:48 on thinkreto
# -------------------------------------------------------------------


import logging
log = logging.getLogger("PySweave.TFH")

class texFileHandler( object ):

   def __init__( self, file, clean=False ):

      import sys, os, pkg_resources
      from glob import glob

      self.clean      = clean
      self.source     = file
      self.postfix    = os.path.splitext( self.source )[1]

      if not self.postfix.lower() in [".rnw",".tex"]:
         log.info("Sorry, currently only .Rnw and .tex files are allowed.")
         sys.exit(3)
   
      self.docfile    = file.replace( self.postfix, "_doc{:s}".format(self.postfix))
      self.beamerfile = file.replace( self.postfix, "_slides{:s}".format(self.postfix))

      log.info("texFileHandler object")
      log.info("  source:       {:s}".format( self.source      ))
      log.info("  doc file:     {:s}".format( self.docfile     ))
      log.info("  beamer file:  {:s}".format( self.beamerfile  ))

      # If clean is set to True: keep names in this folder
      if self.clean:
         self.keep_files = glob("*")
         self.keep_files += [self.docfile.replace( self.postfix, ".pdf"), \
                             self.beamerfile.replace( self.postfix, ".pdf") ]
      else:
         self.keep_files = None

      if not os.path.isfile( self.source ):
         log.info("Input file \"{:s}\" does not exist".format(self.source)); sys.exit(9)

      # Reading source file
      self.config,self.content = self.__read_source_file__()
      self.slidescontent = self.__get_slides_content__()
      self.doccontent    = self.__get_doc_content__()

   def __read_source_file__( self ):

      #content = "".join(open(self.source,"r").readlines()).replace("\n","#").split("#")
      fid     = open(self.source,"r")
      content = "".join(fid.readlines())
      fid.close()

      import sys, re
      res = {}

      # Reading headers. Required, stop if problems occur.
      try:
         res["latex header"]  = re.findall("\[latex\sheader\](.*?)\[/latex\sheader\]",content,re.S)[0]
      except Exception as e:
         log.error(e)
         log.error("Problems reading \"[latex header]\" configuration. Required. Stop."); sys.exit(9)
      try:
         res["beamer header"] = re.findall("\[beamer\sheader\](.*?)\[/beamer\sheader\]",content,re.S)[0]
      except Exception as e:
         log.error(e)
         log.error("Problems reading \"[beamer header]\" configuration. Required. Stop."); sys.exit(9)
      # The footer is not required. If we cannot find the footer
      # we will simply use \end{document} as default.
      try:
         res["latex footer"]  = re.findall("\[latex\sfooter\](.*?)\[/latex\sfooter\]",content,re.S)[0]
      except:
         res["latex footer"]  = "\n\\end{document}\n"
      try:
         res["beamer footer"] = re.findall("\[beamer\sfooter\](.*?)\[/beamer\sfooter\]",content,re.S)[0]
      except:
         res["beamer footer"]  = "\n\\end{document}\n"

      # Replace header/footer tags
      remove = ["latex header","latex footer","beamer header","beamer footer"]
      for rec in remove:
         REGEX = r"(\[{0:s}\].*?\[/{0:s}\]\n?)".format(rec)
         mtch = re.findall( REGEX, content, flags=re.DOTALL )
         for m in mtch: content = content.replace(m,"")

      content = content.split("\n")
      return res,content


   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def showConfig( self ):
      print self.config
      for key,val in self.config.iteritems():
         log.info(" --------- {:s} ----------".format(key))
         for l in val.split("\n"): log.info("   {:s}".format(l))

   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def __get_slides_content__( self ):

      import re
      tmp = "\n".join(self.content)
      # Remove doc content
      REGEX = r"(\\begin{doc}.*?\\end{doc})"
      mtch = re.findall( REGEX, tmp, flags=re.DOTALL )
      for m in mtch: tmp = tmp.replace(m,"")
      #tmp = re.sub(r"\s+?\\begin{doc}.*\s+?\\end{doc}(?=\\end{doc})","",tmp,flags=re.S) 
      # Delete the slides tags
      tmp = re.sub(r"\s+?\\begin\{slides\}","",tmp)
      tmp = re.sub(r"\s+?\\end\{slides\}","",tmp)
      return tmp.split("\n")

   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def __get_doc_content__( self ):

      import re
      tmp = "\n".join(self.content)
      # Remove slide and frame content
      REGEX = r"(\\begin{slides}.*?\\end{slides})"
      mtch = re.findall( REGEX, tmp, flags=re.DOTALL )
      for m in mtch: tmp = tmp.replace(m,"")
      tmp = re.sub(r"\s+?\\begin{frame}\[.*\]","",tmp)
      tmp = re.sub(r"\s+?\\frametitle\{.*\}","",tmp)
      tmp = re.sub(r"\s+?\\end\{frame\}","\n",tmp)
      # Delete the doc tags
      tmp = re.sub(r"\s+?\\begin\{doc\}","",tmp)
      tmp = re.sub(r"\s+?\\end\{doc\}","",tmp)
      return tmp.split("\n")

   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def show( self, part = None ):
      # Show 'raw' content
      if part is None:
         log.info("---------- Content of document file ----------")
         for line in self.content:
            log.info("    {:s}".format(line))
      elif part == "slides":
         log.info("---------- Content of beamer file ----------")
         for line in self.slidescontent:
            log.info("    {:s}".format(line))
      elif part == "doc":
         log.info("Content for the doc file:")
         for line in self.doccontent:
            log.info("    {:s}".format(line))

   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def write( self, what = None ):
      import sys, os
      if what == "doc":
         log.info("Write document output file now ...")
         tmp = []
         tmp.append( self.config["latex header"] )
         tmp += self.doccontent
         tmp.append( self.config["latex footer"] )

         # Write content
         fid = open( self.docfile, "w" )
         fid.write("\n".join(tmp))
         fid.close()

      elif what == "slides":
         log.info("Write beamer output file now ...")
         tmp = []
         tmp.append( self.config["beamer header"] )
         tmp += self.slidescontent
         tmp.append( self.config["beamer footer"] )

         # Write content
         fid = open( self.beamerfile, "w" )
         fid.write("\n".join(tmp))
         fid.close()

   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def render( self ):

      import os, sys
      import subprocess as sub

      def renderExec( cmd ):
         # Execute the command/render tex/Rnw stuff
         try:
            #p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE) 
            #out,err = p.communicate()
            #log.info("Subprocess return value: {:d}".format(p.returncode))
            p = sub.call(cmd)
         except Exception as e:
            log.error(e)
            log.error("Problem during execution of Sweave/pdflatex/bibtex.")

         # Show error from subprocess if some is logged
         #if err: print err

      # If we have to sweave .............
      if self.postfix.lower() == ".rnw":
         log.info("Rendering sweave/Rnw files now")
         # For both, the docfile and the beamerfile we have to
         # sweave the Rnw file and then compile the resulting tex file.
         for file in [self.docfile, self.beamerfile]:
            log.info("Sweaving {:s}".format(file))
            texfile = file.replace(self.postfix,".tex")
            auxfile = file.replace(self.postfix,".aux")
            
            cmd = ["pdflatex", texfile, "&&",
                   "pdflatex", texfile, "&&",
                   "bibtex",   auxfile, "&&",
                   "pdflatex", texfile]
            log.info("Sweaving now ...")
            renderExec( ["R", "CMD", "Sweave", file] )
            log.info("Executing ...")
            log.info(" ".join(cmd))
            renderExec( cmd )
            renderExec( ["pdflatex", texfile] )

      # Only pdflatex/bibtex if input source is a tex file
      elif self.postfix.lower() == ".tex":
         log.info("Rendering LaTeX files now")
         # For both, the docfile and the beamerfile we have to
         # sweave the Rnw file and then compile the resulting tex file.
         for file in [self.docfile, self.beamerfile]:
            log.info("pdflatexing {:s}".format(file))
            auxfile = file.replace(self.postfix,".aux")
            
            cmd = ["pdflatex", file, "&&",
                   "pdflatex", file, "&&",
                   "bibtex",   auxfile, "&&",
                   "pdflatex", file]
            renderExec( cmd )
            renderExec( ["pdflatex",file] )

      return


   # ----------------------------------------------------------------
   # ----------------------------------------------------------------
   def cleanup( self ):

      from glob import glob
      import os
      if not self.clean: return

      # List files
      log.info("Cleaning files")
      files = glob("*")
      for file in glob("*"):
         if not file in self.keep_files:
            log.debug("Remove file: {:s}".format(file))
            os.remove(file)





