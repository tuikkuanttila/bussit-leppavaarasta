# Bussit Leppävaarasta

Hakee HSL:n API:sta muutaman Leppävaaran pysäkin seuraavat lähdöt.
Valittu pysäkit, jotka itsellä ovat useimmiten käytössä, muita voi
hakea helposti rajapinnasta geocode-requestilla, esim.

request=geocode&key=leppavaara&loctypes=stop&city=Espoo&format=txt 

Käytössä Python 3, CherryPy ja Jinja2-templatet.