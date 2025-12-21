#AES vault applikation, som kører en simpel symmetrisk kryptering af filer til vault

Projektet er simpelt, men meget arbejde blev brugt på arkitektonisk overvejelse. 
- primært udviklet som et læringsprojekt
- sekundært udviklet fordi jeg er doven og magter ikke bruge min tid på at finde glemte adgangskoder

Formål: 
- Implementere korrekt AES-baseret kryptering og dekryptering
- implementere en intuitiv brugergrænseflade
- eksperimentere med password-baseret nøgleafledning (KDF)
- skabe noget der kan videreudvikles, når man engang får tid.. 

Funktionalitet
- Kryptering og dekryptering af vilkårlige filer
- AES-128 symmetrisk kryptering
- Initialization vector pr kryptering
- password-basret nøgleafledning (Key Derivate Function)
- single-file vault (.vault)
- session basret arbejdemiljø (RAM)
- grafisk brugergrænseflade

Følgende funktionalitet er planlagt, men midlertidigt latt på hylden
- Import af hele mapper (rekursiv indlæsning af filstruktur)
- Bevarelse af mappestruktur inde i vaulten
- Selektiv eksport af filer eller mapper fra vault
