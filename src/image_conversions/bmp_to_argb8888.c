/* convert an image in bmp format to the 32 bit argb8888 raw format        */
/* argb8888: 8 bits red,green,blue,opacity                                 */ 
/* Written for the course on IoT at the University of Cape Coast, Ghana    */
/* Copyright: U. Raich                                                     */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct __attribute__((packed)) {
  unsigned short type;                     /* Magic identifier            */
  unsigned int size;                       /* File size in bytes          */
  unsigned int reserved;
  unsigned int offset;                     /* Offset to image data, bytes */
} HEADER;

typedef struct __attribute__((packed)) { 
  unsigned int size;               /* Header size in bytes      */
  int width,height;                /* Width and height of image */
  unsigned short planes;           /* Number of colour planes   */
  unsigned short bits;             /* Bits per pixel            */
  unsigned int compression;        /* Compression type          */
  unsigned int imagesize;          /* Image size in bytes       */
  int xresolution,yresolution;     /* Pixels per meter          */
  unsigned int ncolours;           /* Number of colours         */
  unsigned int importantcolours;   /* Important colours         */
  unsigned int dummy;  
} INFOHEADER;

int main(int argc, char ** argv) {
  FILE *inFile,*outFile;
  uint8_t *inbuf,*inbufPtr;
  char *outfileName,*filenameRest;
  HEADER header;
  INFOHEADER infoheader;
  int fileSize;
  if (argc != 2) {
    printf("Usage: %s filename_argb8888.bmp\n",argv[0]);
    exit(-1);
  }
  outfileName = malloc(strlen(argv[1]));
  strcpy(outfileName,argv[1]);
  if ((filenameRest=strstr(outfileName,"_argb8888.bmp")) == NULL) {
    printf("outfileName: %s\n",outfileName);
    printf("File must be named xxx_argb8888.bmp\n");
    exit(-1);
  }
  printf("filename ext: %s\n",filenameRest);
  strcpy(filenameRest,"_argb8888.bin");
  printf("Output file name: %s\n",outfileName);

  if ((inFile = fopen(argv[1],"r")) == NULL)
    fprintf(stderr,"Could not open the %s file for writing\n",argv[1]);
  printf("raw image file successfully opened for reading\n");
  
  fseek(inFile, 0L, SEEK_END);
  fileSize = ftell(inFile);
  printf("file size: %d\n",fileSize);
  rewind(inFile);
  inbuf = malloc(fileSize);
  /*
    read the bmp data
  */
  fread(inbuf, fileSize, 1, inFile);
  fclose(inFile);
  /*
    open the bin file
  */

  inbufPtr = inbuf;
  bcopy(inbufPtr,&header,sizeof(HEADER));
  inbufPtr += sizeof(HEADER);
  bcopy(inbufPtr, &infoheader,sizeof(INFOHEADER));
  printf("Magic: %c%c\n",header.type&0xff,(header.type&0xff00)>>8);
  printf("File size: 0x%04x\n",header.size);
  printf("pixel offset: 0x%04x\n",header.offset);
    
  inbufPtr = inbuf + header.offset;  

  printf("Writing to %s\n",outfileName);
  if ((outFile = fopen(outfileName,"w")) == NULL)
    fprintf(stderr,"Could not open the %s file for writing\n",outfileName);
  printf("bmp image file successfully opened for writing\n");
  if (fwrite(inbufPtr,header.size - header.offset, 1, outFile) != 1)
    printf("error writing pixel information\n");
  fclose(outFile);

}
