#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct link{
	struct link* next;
	char x[33];
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

int power(int x, int y){
	int i;
	int sum;
	sum=1;
	for(i=0;i<y;i++){
		sum*=x;
		
	}
	
	return sum;
}

int bin2int(char *bin, int i){
	int sum;
	char c;
	if (i > 0){
		sum = bin2int(bin, i-1);
	}
	//fprintf(output, "%c", (r==0?'0':'1'));
	c = bin[i];
	sum += atoi(&c) * power(2, 31-i);
	return sum;
}

int main(int argc, char* argv[]){
	FILE *input, *output;
	struct link *a, *t, *head, *temp, *temp2;
	char bin[33];
	int i;
	input = InitInput(argv[1]);
	output = InitOut(argv[2]);
	a = (struct link*)malloc(sizeof(link));
	a->next = NULL;
	head = a;
	
	while(fscanf(input,"%s",&a->x)==1){
		//printf("%s\n",a->x);
		t = (struct link*)malloc(sizeof(link));
		a->next = t;
		t->next = NULL;
		a = a->next;
		
	}

	for(temp = head; temp->next!= NULL; temp = temp->next){

		trans.y = (unsigned int)bin2int(temp->x, 31);
		//printf("%s\n", bin);
		fprintf(output, "%f\n", trans.x);
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
