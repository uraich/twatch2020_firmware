#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
/*
 * a program to create a bmp file from raw argb8888 data
 * created for a project with the course of embedded systems 
 * at the University of Cape Coast, Ghana
 * Author: U. Raich, 21. 12. 2020
 * This program is released under GPL
 */
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
  FILE *inFile;
  uint8_t *inbuf,*inbufPtr;
  HEADER header;
  INFOHEADER infoheader;
  int fileSize;
  if (argc != 2) {
    printf("Usage: %s filename_argb8888.bmp\n",argv[0]);
    exit(-1);
  }

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

  printf("Header size: %d\n",infoheader.size);
  printf("Image width: %d, height: %d\n",infoheader.width,infoheader.height);
  printf("planes: %d\n",infoheader.planes);
  printf("compression: %d\n",infoheader.compression);
  printf("imagesize: %d\n",infoheader.imagesize);
  printf("xresolution: %d yresolution %d\n",infoheader.xresolution,infoheader.xresolution);
  printf("ncolors: %d\n",infoheader.ncolours);
  
  
    
}
