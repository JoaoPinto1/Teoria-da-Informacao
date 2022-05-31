#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define N		 4096	/* tamanho do buffer circular */
#define F		   18	/* limite máximo para match_length */
#define THRESHOLD	2   /* codificação da string num par (offset, tamanho)
						   se match_length for maior que THRESHOLD */
#define NIL			N	/* indice para a raiz de uma binary search trees */

unsigned long int
                textsize = 0,	/* contador para o tamanho do texto */
                codesize = 0,	/* contador do tamanho do código */
                printcount = 0;	/* contador para verificar o progresso a cada 1Kbyte */
unsigned char
                text_buf[N + F - 1];	/* buffer circular de tamanho N,
                com F-1 bytes extra para facilitar a comparação de strings */
int		        match_position, match_length,  /* da correspondencia mais longa. Este são
			definidos pelo procedimento InsertNode(). */
                lson[N + 1], rson[N + 257], dad[N + 1];  /* filho esquerdo e direito &
			pai -- constituem as binary search trees. */
FILE	*infile , *outfile;  /* input & output files */

void InitTree(void){  /* inicialização das árvores */
    int  i;

    /* Para i = 0 até N - 1, rson[i] and lson[i] vão ser o filho direito e esquerdo
       do nodo i.  Este nodos não precisam de ser inicializados.
       Também, dad[i] é o pai do nodo i.  Estes são inicializados a
       NIL (= N), que significa 'não usado'.
       Para i = 0 até 255, rson[N + i + 1] é a raiz da árvore
       para strings que começam com o caracter i. Estes são inicializados a
       NIL. */

    for (i = N + 1; i <= N + 256; i++) rson[i] = NIL;
    for (i = 0; i < N; i++) dad[i] = NIL;
}

void InsertNode(int r)
/* Insere uma string de tamanho F, text_buf[r..r+F-1], numa das árvores
   (text_buf[r] árvore) e retorna a maior correspondencia atraves das
   variaveis globais match_position and match_length.
   Se match_length = F, então remove o antigo nodo e insere o novo,
   porque o antigo será eliminado anteriormente. */
{
    int  i, p, cmp;
    unsigned char  *key;

    cmp = 1;  key = &text_buf[r];  p = N + 1 + key[0];
    rson[r] = lson[r] = NIL;  match_length = 0;
    for ( ; ; ) {
        if (cmp >= 0) {
            if (rson[p] != NIL) p = rson[p];
            else {  rson[p] = r;  dad[r] = p;  return;  }
        } else {
            if (lson[p] != NIL) p = lson[p];
            else {  lson[p] = r;  dad[r] = p;  return;  }
        }
        for (i = 1; i < F; i++)
            if ((cmp = key[i] - text_buf[p + i]) != 0)  break;
        if (i > match_length) {
            match_position = p;
            if ((match_length = i) >= F)  break;
        }
    }
    dad[r] = dad[p];  lson[r] = lson[p];  rson[r] = rson[p];
    dad[lson[p]] = r;  dad[rson[p]] = r;
    if (rson[dad[p]] == p) rson[dad[p]] = r;
    else                   lson[dad[p]] = r;
    dad[p] = NIL;  /* remover p */
}

void DeleteNode(int p)  /* elimina o nodo p da árvore */
{
    int  q;

    if (dad[p] == NIL) return;  /* não está na árvore */
    if (rson[p] == NIL) q = lson[p];
    else if (lson[p] == NIL) q = rson[p];
    else {
        q = lson[p];
        if (rson[q] != NIL) {
            do {  q = rson[q];  } while (rson[q] != NIL);
            rson[dad[q]] = lson[q];  dad[lson[q]] = dad[q];
            lson[q] = lson[p];  dad[lson[p]] = q;
        }
        rson[q] = rson[p];  dad[rson[p]] = q;
    }
    dad[q] = dad[p];
    if (rson[dad[p]] == p) rson[dad[p]] = q;  else lson[dad[p]] = q;
    dad[p] = NIL;
}

void Encode(void)
{
    clock_t begin = clock();
    int  i, c, len, r, s, last_match_length, code_buf_ptr;
    unsigned char  code_buf[17], mask;

    InitTree();  /* inicializar as árvores */
    code_buf[0] = 0;  /* code_buf[1..16] salva 8 unidades de código, e
		code_buf[0] funciona como 8 flags, "1" respresenta que a unidade
		é uma letra não codificada (1 byte), "0" representa um par(offset, tamanho)
		(2 bytes).  Assim sendo, 8 unidades de códigos ncessitam no máximo 16bytes de código. */
    code_buf_ptr = mask = 1;
    s = 0;  r = N - F;
    for (i = s; i < r; i++) text_buf[i] = ' ';  /* Clear the buffer with
		any character that will appear often. */
    for (len = 0; len < F && (c = getc(infile)) != EOF; len++)
        text_buf[r + len] = c;  /* Read F bytes into the last F bytes of
			the buffer */
    if ((textsize = len) == 0) return;  /* text of size zero */
    for (i = 1; i <= F; i++) InsertNode(r - i);  /* Insert the F strings,
		each of which begins with one or more 'space' characters.  Note
		the order in which these strings are inserted.  This way,
		degenerate trees will be less likely to occur. */
    InsertNode(r);  /* Finally, insert the whole string just read.  The
		global variables match_length and match_position are set. */
    do {
        if (match_length > len) match_length = len;  /* match_length
			pode muito grande a medida que se aproxima o final do texto. */
        if (match_length <= THRESHOLD) {
            match_length = 1;  /* Correspondencia não é grande o suficiente. Enviar 1 byte. */
            code_buf[0] |= mask;  /* 'Enviar 1 byte' flag */
            code_buf[code_buf_ptr++] = text_buf[r];  /* Enviar sem codificação. */
        } else {
            code_buf[code_buf_ptr++] = (unsigned char) match_position;
            code_buf[code_buf_ptr++] = (unsigned char)
                    (((match_position >> 4) & 0xf0)
                     | (match_length - (THRESHOLD + 1)));  /* Enviar o par (offset, tamanho). */
        }
        if ((mask <<= 1) == 0) {  /* Deslocar a máscara 1bit. */
            for (i = 0; i < code_buf_ptr; i++)  /* Enviar no máximo 8 unidades de código */
                putc(code_buf[i], outfile);
            codesize += code_buf_ptr;
            code_buf[0] = 0;  code_buf_ptr = mask = 1;
        }
        last_match_length = match_length;
        for (i = 0; i < last_match_length &&
                    (c = getc(infile)) != EOF; i++) {
            DeleteNode(s);		/* Eliminar a string antiga e */
            text_buf[s] = c;	/* ler os novos bytes */
            if (s < F - 1) text_buf[s + N] = c;  /* Se a posição se encontra
				perto do final do buffer, extender o buffer para facilitar a
				comparação da string. */
            s = (s + 1) & (N - 1);  r = (r + 1) & (N - 1);
            /* Sendo um buffer circular, incrementar a posição. */
            InsertNode(r);	/* Inserir a string presente em text_buf[r..r+F-1] na árvore*/
        }
        if ((textsize += i) > printcount) {
            printf("%12ld\r", textsize);  printcount += 1024;
            /* Devolve o estado cada vez que o tamanho do texto exceda
               multiplos de 1024. */
        }
        while (i++ < last_match_length) {	/* Depois de todo o texto ser processado, */
            DeleteNode(s);					/* não há necessidade de ler, mas */
            s = (s + 1) & (N - 1);  r = (r + 1) & (N - 1);
            if (--len) InsertNode(r);		/* o buffer pode não estar vazio. */
        }
    } while (len > 0);	/* Enquanto o tamanho da string a processar ser 0 */
    if (code_buf_ptr > 1) {		/* Enviar o restante código. */
        for (i = 0; i < code_buf_ptr; i++) putc(code_buf[i], outfile);
        codesize += code_buf_ptr;
    }
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Time: %f segundos\n",time_spent);

    printf("In : %ld bytes\n", textsize/*in*/);	/* Concluída a codificação */
    printf("Out: %ld bytes\n", codesize/*ou*/);
    printf("Out/In: %.3f\n", (textsize-(double)codesize)/textsize);
}

void Decode(void)	/* Processo inverso à função Encode(). */
{
    clock_t begin = clock();
    int  i, j, k, r, c;
    unsigned int  flags;

    for (i = 0; i < N - F; i++) text_buf[i] = ' ';
    r = N - F;  flags = 0;
    for ( ; ; ) {
        if (((flags >>= 1) & 256) == 0) {
            if ((c = getc(infile)) == EOF) break;
            flags = c | 0xff00;		/* contagem das flags até 8 */
        }
        if (flags & 1) {
            if ((c = getc(infile)) == EOF) break;
            putc(c, outfile);  text_buf[r++] = c;  r &= (N - 1);
        } else {
            if ((i = getc(infile)) == EOF) break;
            if ((j = getc(infile)) == EOF) break;
            i |= ((j & 0xf0) << 4);  j = (j & 0x0f) + THRESHOLD;
            for (k = 0; k <= j; k++) {
                c = text_buf[(i + k) & (N - 1)];
                putc(c, outfile);  text_buf[r++] = c;  r &= (N - 1);
            }
        }
    }
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Time: %f segundos\n",time_spent);
}

int main(int argc, char *argv[])
{
    
    infile = fopen("comprimido.txt", "rb");
    outfile = fopen("original.txt", "wb");

   Encode();
   //Decode();

    fclose(infile);  fclose(outfile);


}

