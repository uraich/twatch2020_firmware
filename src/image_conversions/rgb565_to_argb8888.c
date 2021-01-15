/* Convert an image in rgb565:  5 bits red, 6 bits blue, 5 bits green      */
/* to argb8888 format: (8 bits for red,green,blue,opacity)                 */
/* Written for the course on IoT at the University of Cape Coast, Ghana    */
/* Copyright: U. Raich                                                     */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char ** argv){
  FILE *infile,*outfile;
  char *outfileName;
  char *filenameRest;
  unsigned char red,green,blue;
  unsigned char *inbuf,*outbuf,*inbufPtr,*outbufPtr;
  int fileSize,i;

  if (argc != 2) {
    printf("Usage: %s filename width height\n",argv[0]);
    exit(-1);
  }
  outfileName = malloc(strlen(argv[1])+2);
  strcpy(outfileName,argv[1]);
  if ((filenameRest=strstr(outfileName,"_rgb565.bin")) == NULL) {
    printf("File must be named xxx_rgb565.bin");
    exit(-1);
  }
  printf("filename base: %s\n",filenameRest);
  strcpy(filenameRest,"_argb8888.bin");
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
  outbuf = malloc(fileSize*2);
  
  fread(inbuf, fileSize, 1, infile);
  fclose(infile);
    
  for (i=0; i<16;i++)
    printf("0x%02x ",inbuf[i]);
  printf("\n");
    
  inbufPtr = inbuf;
  outbufPtr = outbuf;
  
  for (i=0;i<fileSize;i+=2) {
    red = *inbufPtr++;
    // printf("col high: %02x\n",red);
    green = (red & 7) << 5;
    blue = *inbufPtr++;
    // printf("col low: %02x\n",blue);   
    green |= (blue & 0xe0)>> 3;
    green |= 3;
    red |= 7;
    blue = (blue << 3) | 7;
    
    // printf("red: %02x, green: %02x, blue: %02x\n",red,green,blue);    
    *outbufPtr++ = blue; // the color
    *outbufPtr++ = green;
    *outbufPtr++ = red;
    *outbufPtr++ = 0xff; // cover
  }

  outfile = fopen(outfileName,"w");
  if (outfile == NULL) {
    printf("Could not open %s for writing",outfileName);
    exit(-1);
  }
  fwrite(outbuf, fileSize*2, 1, outfile);
  fclose(outfile);
    
}
