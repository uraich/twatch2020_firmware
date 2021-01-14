#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
/*
 * a program to create a bmp file from raw argb8888 data
 * created for a project with the course of embedded systems 
 * at the University of Cape Coast, Ghana
 * Author: U. Raich, 21. 12. 2020
 * This program is released under the MIT license
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
  FILE *inFile,*outFile;
  uint8_t *inbuf;
  char *outfileName,*filenameRest;
  HEADER header;
  INFOHEADER infoheader;
  int fileSize,width,height;
  if (argc != 4) {
    printf("Usage: %s filename_argb8888.bin width height\n",argv[0]);
    exit(-1);
  }
  outfileName = malloc(strlen(argv[1]));
  strcpy(outfileName,argv[1]);
  if ((filenameRest=strstr(outfileName,"_argb8888.bin")) == NULL) {
    printf("outfileName: %s\n",outfileName);
    printf("File must be named xxx_argb8888.bin\n");
    exit(-1);
  }
  printf("filename ext: %s\n",filenameRest);
  strcpy(filenameRest,"_argb8888.bmp");
  printf("Output file name: %s\n",outfileName);
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
    open the bmp file
  */
  printf("Writing to %s\n",outfileName);
  if ((outFile = fopen(outfileName,"w")) == NULL)
    fprintf(stderr,"Could not open the %s file for writing\n",outfileName);
  printf("bmp image file successfully opened for writing\n");
  
  header.type=0x4d42;                /* corresponds to "BM" */
  header.size=sizeof(HEADER)+sizeof(INFOHEADER)+256*288*3;
  //  header.size=0x30876;
  header.reserved=0;
  header.offset=sizeof(HEADER) + sizeof(INFOHEADER);
  printf("pixel offset is: %d\n",header.offset);

  if (fwrite(&header,sizeof(HEADER),1,outFile) != 1)
    fprintf(stderr,"header was not written\n");
  else
    printf("BMP header was successfull written\n");
  
  infoheader.size=40;
  infoheader.width=width;
  infoheader.height=height;
  //  infoheader.width=245;
  //  infoheader.height=270;
  infoheader.planes=1;
  infoheader.bits=32;
  infoheader.compression=0;
  infoheader.imagesize=width*height;
  infoheader.xresolution=2834;
  infoheader.yresolution=2834;
  infoheader.ncolours=0;
  infoheader.importantcolours=0;

  printf("resolution: x: 0x%08x y: 0x%08x\n",
	 infoheader.xresolution,
	 infoheader.yresolution);
  
  if (fwrite(&infoheader,sizeof(INFOHEADER),1,outFile) != 1)
    fprintf(stderr,"infoheader was written\n");
  else
    printf("BMP infoheader was successfully written\n"); 

//  fseek(fd,40,SEEK_SET);
  if (fwrite(inbuf,width*height*4,1,outFile) != 1)
    printf("error writing pixel information\n");

  fclose(outFile);

}
