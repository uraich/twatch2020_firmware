#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
/*
 * a program to create a micropython file from raw argb8888 data
 * created for a project with the course of embedded systems 
 * at the University of Cape Coast, Ghana
 * Author: U. Raich, 21. 12. 2020
 * This program is released under GPL
 */

int main(int argc, char ** argv) {
  FILE *inFile,*outFile;
  uint8_t *inbuf,*inbufPtr;
  char *outfileName,*filenameRest,*basename,*basenamePtr;
  int i,fileSize,width,height;
  
  if (argc != 4) {
    printf("Usage: %s filename_argb8888.bin width height\n",argv[0]);
    exit(-1);
  }
  outfileName = malloc(strlen(argv[1]));
  basename = malloc(strlen(argv[1]));
  
  strcpy(basename,argv[1]);
  strcpy(outfileName,argv[1]);

  if ((filenameRest=strstr(outfileName,"_argb8888.bin")) == NULL) {
    printf("outfileName: %s\n",outfileName);
    printf("File must be named xxx_argb8888.bin\n");
    exit(-1);
  }
  printf("filename ext: %s\n",filenameRest);
  strcpy(filenameRest,"_argb8888.py");
  printf("Output file name: %s\n",outfileName);
  basenamePtr = strstr(basename,"_argb8888.bin");
  *basenamePtr = '\0';
  printf("basename: %s\n",basename);
    
  width = atoi(argv[2]);
  height = atoi(argv[3]);
  printf("width: %d, height: %d\n",width,height);      
  if ((inFile = fopen(argv[1],"r")) == NULL)
    fprintf(stderr,"Could not open the %s file for writing\n",argv[1]);
  printf("raw image file successfully opened for reading\n");
  
  fseek(inFile, 0L, SEEK_END);
  fileSize = ftell(inFile);
  printf("file size: %d\n",fileSize);
  rewind(inFile);
  inbuf = malloc(fileSize);
  /*
    read the raw data
  */
  fread(inbuf, fileSize, 1, inFile);
  fclose(inFile);
  /*
    open the micropython file
  */
  printf("Writing to %s\n",outfileName);
  if ((outFile = fopen(outfileName,"w")) == NULL)
    fprintf(stderr,"Could not open the %s file for writing\n",outfileName);
  fprintf(outFile,"#\n# initialize lvgl\n#\n");
  printf("bmp image file successfully opened for writing\n");
  fprintf(outFile,"import lvgl as lv\n\n");

  fprintf(outFile,"%s_img_data = b'",basename);
  inbufPtr = inbuf;
  for (i=0;i<fileSize;i++) 
    fprintf(outFile,"\\x%02x",*inbufPtr++);
  fprintf(outFile,"'\n\n");
  fprintf(outFile,"%s_img_dsc = lv.img_dsc_t(\n\t{\n",basename);
  fprintf(outFile,"\t\t\"header\": {\"always_zero\": 0, \"w\": %d, \"h\": %d, \"cf\": lv.img.CF.TRUE_COLOR_ALPHA},\n",
	  width,height);
  fprintf(outFile,"\t\t\"data\": %s_img_data,\n",basename);
  fprintf(outFile,"\t\t\"data_size\": len(%s_img_data),\n",basename);
  fprintf(outFile,"\t}\n)\n\n");
    
  fclose(outFile);

}
