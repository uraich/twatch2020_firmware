/* Convert an image in argb8888 format (8 bits for red,green,blue,opacity)  */
/* to argb565 format: 5 bits red, 6 bits blue, 5 bits green, 8 bits opacity */
/* Written for the course on IoT at the University of Cape Coast, Ghana     */
/* Copyright: U. Raich                                                      */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char ** argv){
  FILE *infile,*outfile;
  char *outfileName,*filenameRest;
  unsigned char *inbuf,*outbuf,*inbufPtr,*outbufPtr;
  unsigned char red,green,blue,opacity,col_high_byte,col_low_byte;
  int i,fileSize;
  
  if (argc != 2) {
    printf("Usage: %s filename\n",argv[0]);
    exit(-1);
  }
  outfileName = malloc(strlen(argv[1])-1);
  strcpy(outfileName,argv[1]);
  if ((filenameRest=strstr(outfileName,"_argb8888.bin")) == NULL) {
    printf("File must be named xxx_argb8888.bin");
    exit(-1);
  }
  printf("filename base: %s\n",filenameRest);
  strcpy(filenameRest,"_argb565.bin");
  printf("Output file name: %s\n",outfileName);

  infile = fopen(argv[1],"r");
  if (infile == NULL) {
    printf("Could not open %s\n",argv[1]);
    exit(-1);
  }

  fseek(infile, 0L, SEEK_END);
  fileSize = ftell(infile);
  printf("file size: %d\n",fileSize);
  rewind(infile);

  inbuf = malloc(fileSize);
  outbuf = malloc(fileSize*3/4);

  fread(inbuf, fileSize, 1, infile);
  fclose(infile);


    
  for (i=0; i<16;i++)
    printf("0x%02x ",inbuf[i]);
  printf("\n");
    
  inbufPtr = inbuf;
  outbufPtr = outbuf;
  for (i=0;i<fileSize/4;i++) {
// for (i=0;i<1;i++) {
    blue = *inbufPtr++;
    green = *inbufPtr++;
    red = *inbufPtr++;
    opacity = *inbufPtr++;  

    red &=0xf8;
    green &=0xfc;
    blue &=0xf8;
    col_high_byte = red | (green & 0xe0) >> 5;
    col_low_byte = (green & 0x1c) << 3 | blue >> 3;
    //    printf("red: 0x%02x, green: 0x%02x, blue: 0x%02x, high: 0x%02x, low: 0x%02x\n",
    //	   red,green,blue,col_high_byte,col_low_byte);

    *outbufPtr++ = col_high_byte;
    *outbufPtr++ = col_low_byte;
    *outbufPtr++ = opacity;
  }
  outfile = fopen(outfileName,"w");
  if (outfile == NULL) {
    printf("Could not open %s",outfileName);
    exit(-1);
  }
  fwrite(outbuf, fileSize*3/4, 1, outfile);
  fclose(outfile);
    
}
