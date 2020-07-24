# Muzeeglot

In this repository, we present [Muzeeglot](https://research.deezer.com/muzeeglot), a propotype aiming at illustrating how
multilingual music genre embedding space representations can be leveraged to
**generate cross-lingual music genre annotations** for
[DBpedia](https://wiki.dbpedia.org/) music entities (artists, albums, tracks...).

<div align="center">
    <img
        src="https://github.com/deezer/muzeeglot/blob/master/screenshot.png?raw=true"
        width="70%">
    <p>
        <a href="https://research.deezer.com/muzeeglot">Muzeeglot</a> includes a web interface to visualize these
        multilingual music genre embeddings.
    </p>
</div>

Based on annotations from one or several sources languages, our system automatically
predicts the corresponding annotations in a target language.

Languages supported:

- French (fr)
- English (en)
- Spanish (es)
- Dutch (nl)
- Czech (cs)
- Japanese (ja)

## Technical Details

[Muzeeglot](https://research.deezer.com/muzeeglot) will be presented as a demonstration at [JEP-TALN-RECITAL 2020](https://jep-taln2020.loria.fr).

This [extended abstract](https://jep-taln2020.loria.fr/wp-content/uploads/JEP-TALN-RECITAL-2020_paper_156.pdf) (in French) from the conference provides more information on [Muzeeglot](https://research.deezer.com/muzeeglot). Feel free to also check out those [slides](https://github.com/deezer/muzeeglot/blob/master/presentation.pdf) for more information in English.

## Demonstration

The demo is currently live [here](https://research.deezer.com/muzeeglot).

In this repository, we will also soon release the source code of Muzeeglot.


## Cite

```BibTeX
@inproceedings{epure2020muzeeglot,
  title={Muzeeglot: annotation multilingue et multi-sources d'entit{\'e}s musicales {\`a} partir de repr{\'e}sentations de genres musicaux},
  author={Epure, Elena V and Salha, Guillaume and Voituret, F{\'e}lix and Baranes, Marion and Hennequin, Romain},
  booktitle={Actes de la 6e conf{\'e}rence conjointe Journ{\'e}es d'{\'E}tudes sur la Parole (JEP, 31e {\'e}dition), Traitement Automatique des Langues Naturelles (TALN, 27e {\'e}dition), Rencontre des {\'E}tudiants Chercheurs en Informatique pour le Traitement Automatique des Langues (R{\'E}CITAL, 22e {\'e}dition). Volume 4: D{\'e}monstrations et r{\'e}sum{\'e}s d'articles internationaux},
  pages={18--21},
  year={2020},
  organization={ATALA}
}
```
