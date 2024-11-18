#include <stdio.h>
#include <stdlib.h>

#define  MAX_AFETZEDE_SAYISI 100
#define  MAX_ISIM_UZUNLUK  28
#define  MAX_TELEFON_UZUNLUK  15
#define  MAX_ADRES_UZUNLUK  200
#define  MAX_TALEP_UZUNLUK 300
#define  MAX_TALEP_SAYISI 300

char afetzede_isimleri[MAX_AFETZEDE_SAYISI][MAX_ISIM_UZUNLUK];
char afetzede_soyisimleri[MAX_AFETZEDE_SAYISI][MAX_ISIM_UZUNLUK];
char afetzede_telefonlari[MAX_AFETZEDE_SAYISI][MAX_TELEFON_UZUNLUK];
char afetzede_adresleri[MAX_AFETZEDE_SAYISI][MAX_ADRES_UZUNLUK];
char talep_aciklamalari[MAX_AFETZEDE_SAYISI][MAX_TALEP_UZUNLUK];
char talep_afetzede_idleri[MAX_TALEP_SAYISI];
int afetzede_sayisi=0;
int talep_sayisi=0;
void afetzede_ekle(char *adi,char *soyadi,char *telefonu,char *adresi){
    if (afetzede_sayisi >= MAX_AFETZEDE_SAYISI) {
        hata_mesaji();
        return;
    }
	for(int c=0;c<MAX_ISIM_UZUNLUK;c++)
	{
		afetzede_isimleri[afetzede_sayisi][c]=adi[c];
		afetzede_soyisimleri[afetzede_sayisi][c]=soyadi[c];
		afetzede_telefonlari[afetzede_sayisi][c]=telefonu[c];
		afetzede_adresleri[afetzede_sayisi][c]=adresi[c];
		
	}
	printf("Afetzedenin Id' si=%d\n",afetzede_sayisi);
	printf("Afetzede kaydi yapildi\n");	
	printf("\n\n");
}

void afetzede_guncelleme(int id,char *adi,char *soyadi,char *telefonu,char *adresi){	
 	printf("\n\n");
	for(int c=0;c<MAX_ISIM_UZUNLUK;c++)
	{	
		if (id < 0 || id > afetzede_sayisi) {
        hata_mesaji();
        break;
		}
		afetzede_isimleri[id][c]=adi[c];
		afetzede_soyisimleri[id][c]=soyadi[c];
		afetzede_telefonlari[id][c]=telefonu[c];
		afetzede_adresleri[id][c]=adresi[c]; 
	}
	printf("\n\n");
}

void afetzede_sil(int id){
	if (id < 0 || id > afetzede_sayisi) {
        hata_mesaji();
        return;
       }
     else{
        	printf("Afetzede silindi\n");
		 }
	for(int c=0;c<MAX_ISIM_UZUNLUK;c++)
	{	afetzede_isimleri[id][c]=NULL;
		afetzede_soyisimleri[id][c]=NULL;
		afetzede_telefonlari[id][c]=NULL;
		afetzede_adresleri[id][c]=NULL;
	}
	printf("\n\n");
}

void yardim_talebi_kaydet(int id, char* aciklamasi) {
    if (id < 0 || id >= MAX_TALEP_SAYISI) {
        hata_mesaji("Geçersiz talep ID'si.");
        return;
    }
    for (int i = 0; i < MAX_TALEP_UZUNLUK; i++) {
        talep_aciklamalari[id][i] = aciklamasi[i];
    }
    printf("\n\n");
}

void afetzede_listeleme(){
	printf("\n\n");
	for(int i=0;i<=afetzede_sayisi;i++){
		if(afetzede_isimleri[i][0]!=NULL){
			printf("Afetzede listesi:\n");
			printf("Afetzedinin ID' si:%d\n",i);
			printf("Afetzedenin adi:%s\n",afetzede_isimleri[i]);
			printf("Afetzedenin soyadi:%s\n",afetzede_soyisimleri[i]);
			printf("Afetzedenin telefonu:%s\n",afetzede_telefonlari[i]);
			printf("Afetzedenin adresi:%s\n",afetzede_adresleri[i]);
			printf("\n");
		}
	}
	printf("\n\n");
}

void afetzede_ara(int id){	
 	if (id < 0 || id > afetzede_sayisi) {
        hata_mesaji();
        return;
    }
	printf("Afetzede ismi:%s\n",afetzede_isimleri[id]);
	printf("Afetzede soyismi:%s\n",afetzede_soyisimleri[id]);
	printf("Afetzede telefonu:%s\n",afetzede_telefonlari[id]);
	printf("Afetzede adresi:%s\n",afetzede_adresleri[id]);
	printf("\n\n");
}

void yardim_talepleri_listeleme(){

		for(int c=0;c<=MAX_TALEP_SAYISI;c++)
		{
			if(talep_aciklamalari[c][0]!=NULL)
			{
				printf("Afetzede idsi:%d",c);
				printf("AFetzede talebi:%s\n",talep_aciklamalari[c]);
			}
		}
		printf("\n\n");
}

void menu_goster(){
	printf("			1-Afetzede Ekle\n");
	printf("			2-Afetzede Guncelle\n");
	printf("			3-Afetzede Sil\n");
	printf("			4-Afetzede Talebi Kaydet\n");
	printf("			5-Afetzede Listeleme\n");
	printf("			6-Afetzede Ara\n");
	printf("			7-Afetzede Talepleri Listeleme\n");
	printf("			0-Cikis\n");
	printf("	----------------------------------------------------------\n");
	printf("  		    Yapmak istediginiz islemi girininiz:");
	}
	
void hata_mesaji(){
	printf("Girdiginiz degerler hatalidir !\n");
}
int main() {

	int id,menu;
	char adi[MAX_ISIM_UZUNLUK],soyadi[MAX_ISIM_UZUNLUK],telefonu[MAX_TELEFON_UZUNLUK],adresi[MAX_ADRES_UZUNLUK],aciklamasi[MAX_TALEP_UZUNLUK];
	
	menu_goster();
	
	do{
		scanf("%d",&menu);
		switch (menu){
			case 1 : 
				printf("Afetzedenin adini giriniz:");
				scanf("%s",adi);
				printf("Afetzedenin soyadini giriniz:");
				scanf("%s",soyadi);
				printf("Afetzedenin telefonunu giriniz:");
				scanf("%s",telefonu);
				printf("Afetzedenin adresini giriniz:");
				scanf("%s",adresi);
				afetzede_sayisi++;
				afetzede_ekle(&adi,&soyadi,&telefonu,&adresi);
				printf("\n");
				menu_goster();
				
				break;
			case 2 :
				printf("Guncellenecek Afezedenin Id 'sini giriniz:");
				scanf("%d",&id);
				printf("Afetzedenin adini giriniz:");
				scanf("%s",adi);
				printf("Afetzedenin soyadini giriniz:");
				scanf("%s",soyadi);
				printf("Afetzedenin telefonunu giriniz:");
				scanf("%s",telefonu);
				printf("Afetzedenin adres giriniz:");
				scanf("%s",adresi);
				afetzede_guncelleme(id,&adi,&soyadi,&telefonu,&adresi);
				printf("\n");
				menu_goster();
				break;
			case 3 :
				printf("Silinecek Afezedenin Id=:");
				scanf("%d",&id);
				afetzede_sil(id);
				printf("\n");
				menu_goster();
				break;
			case 4 :
				printf("Talep Girilecek Afezedenin Id=:");
				scanf("%d",&id);
				printf("Afezedenin Talebi=:");
				scanf("%s",aciklamasi);yardim_talebi_kaydet(id,&aciklamasi);
				printf("\n");
				menu_goster();
				break;	
			case 5 :
				afetzede_listeleme();
				printf("\n");     
				menu_goster();
				break;	
			case 6 :
				printf("Aranacak Afezedenin Id=:");
				scanf("%d",&id);
				afetzede_ara(id);
				printf("\n");
				menu_goster();
				break;
			case 7 :
				yardim_talepleri_listeleme();	
				printf("\n");      
				menu_goster();
				break;}
		}while(menu!=0);
	return 0;
}