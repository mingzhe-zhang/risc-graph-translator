#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct link{
	struct link* next;
	double x;
} link;

union trans{
	float x;
	unsigned int y;
} trans;

FILE* InitOut(char* filename){
	FILE* out;
	out = fopen(filename, "w");
	if(!stdout){
		printf("File name error!\n");
		return;
	}
	return out;
}

FILE* InitInput(char* filename){
	FILE* input;
	input = fopen(filename, "r");
	if(!stdin){
		printf("File name error!\n");
		return;
	}
	return input;
}

void int2bin(unsigned int n, char* bin, int i){
	int r;
	r = n %2;
	if (n >= 2){
		int2bin(n/2, bin, i-1);
	}
	//fprintf(output, "%c", (r==0?'0':'1'));
	bin[i] = (r==0?'0':'1');
	
}

int main(int argc, char* argv[]){
	FILE *input, *output;
	struct link *a, *t, *head, *temp, *temp2;
	char bin[33];
	int i;
	input = InitInput(argv[1]);
	output = InitOut(argv[2]);
	a = (struct link*)malloc(sizeof(link));
	a->x = 0;
	a->next = NULL;
	head = a;
	
	while(fscanf(input,"%lf",&a->x)==1){
		printf("%lf\n",a->x);
		t = (struct link*)malloc(sizeof(link));
		a->next = t;
		t->next = NULL;
		t->x = 0;
		a = a->next;
		
	}
	
	for(i=0;i<33;i++){
		bin[i] = '0';
	}
	bin[32] = '\0';
	for(temp = head; temp->next!= NULL; temp = temp->next){
		trans.x = temp->x;
		int2bin(trans.y, bin, 31);
		//printf("%s\n", bin);
		fprintf(output, "%s\n", bin);
	}
	temp = head;
	do{
		temp2 = temp->next;
		free(temp);
		temp = temp2;
	}while(temp!=NULL);
	
	fclose(input);
	fclose(output);
}
