# Muzeeglot

In this repository, we present [Muzeeglot](https://research.deezer.com/muzeeglot),
a propotype aiming at illustrating how multilingual music genre embedding space
representations can be leveraged to **generate cross-lingual music genre annotations**
for [DBpedia](https://wiki.dbpedia.org/) music entities (artists, albums, tracks, etc ...).

<div align="center">
    <img
        src="https://github.com/deezer/muzeeglot/blob/master/docs/screenshot.png?raw=true"
        width="70%">
    <p>
        <a href="https://research.deezer.com/muzeeglot">Muzeeglot</a> includes a web interface to visualize these
        multilingual music genre embeddings.
    </p>
</div>

- :question: [How it works](#how-it-works)
- :gear: [Architecture](#architecture)
- :rocket: [Deployment](#deployment)
    * :lock: [SSL support](#ssl-support)
- :computer: [Development](#development)
- :book: [Cite](#cite)

## How it works

Based on annotations from one or several source languages, our system automatically
predicts the corresponding annotations in a target language.

Languages supported:

- :fr: French
- :gb: English
- :es: Spanish
- :netherlands: Dutch
- :czech_republic: Czech
- :jp: Japanese

You will find more information about application usage [here](https://github.com/deezer/muzeeglot/blob/master/docs/presentation.pdf).

## Architecture

[Muzeeglot](https://research.deezer.com/muzeeglot) is based on a classic _N-tier_ architecture
including :

- A [Redis](https://redis.io) instance as storage engine.
- A REST API developed in Python with [FastAPI](https://fastapi.tiangolo.com).
- A frontend developed with [VueJS](https://vuejs.org), as a SPA (Single Page Application).

The overall stack is loadbalanced using [Nginx](https://www.nginx.com) webserver :

<div align="center">
    <img
        src="https://github.com/deezer/muzeeglot/blob/master/docs/architecture.png?raw=true">
</div>

Data such as entities, tags, and languages are stored into the [Redis](https://redis.io)
instance. Additionnally, a text search index based on [Whoosh](https://github.com/mchaput/whoosh)
is maintained using _ngram_ tokenization on entity names.

## Deployment 

Deploying [Muzeeglot](https://research.deezer.com/muzeeglot) requires the following tools to be
installed :

- [Git](https://git-scm.com)
- [GNU make](https://www.gnu.org/software/make/)
- [Docker](https://www.docker.io)
- [Docker compose](https://docs.docker.com/compose/)

You can then clone this repository and start [Muzeeglot](https://research.deezer.com/muzeeglot)<sup>1</sup> :

```bash
git clone https://github.com/deezer/muzeeglot
cd muzeeglot
make start
```

Behind the scene it will build the required [docker](https://www.docker.io) images and run a
[compose](https://docs.docker.com/compose/) file with everything required locally in daemon mode.

> <sup>1</sup> first deployment will be long as it requires data ingestion and indexing.

### SSL support

In case you want to deploy [Muzeeglot](https://research.deezer.com/muzeeglot) with SSL
using [LetsEncrypt](https://letsencrypt.org), you need to first create certificate using
the provided bot challenge. Start by editing the following configuration files to add your
target domain :

- `frontend/nginx/certificate-builder.conf`
- `frontend/nginx/muzeeglot-ssl.conf`

Once you did so, you can run the following command to generate SSL certificates:

```bash
make letsencrypt DOMAIN=mydomain.tld
```

It will create a [docker](https://www.docker.io) volume and provision it with certificate.
Then you can run [Muzeeglot](https://research.deezer.com/muzeeglot) as follows:

```bash
make ssl start
```

## Development

Project can be managed using `GNU Make` through the following goals :

| Goal          | Description                                    |
| ------------- | ---------------------------------------------- |
| _api_         | Build api image                                |
| _frontend_    | Build frontend image                           |
| _run_         | Start the entire stack using docker-compose    |
| _start_       | Start the entire stack in daemon mode          |
| _stop_        | Stop the entier stack using docker-compose     |
| _logs_        | Display stack logs when running in daemon mode |
| _clean_       | Clean docker volume for storage and indexes    |
| _letsencrypt_ | Generate certificate volume                    |

Additional goals can be used to provide extra parameters:

| Goal       | Description                          |
| ---------- | ------------------------------------ |
| _no-cache_ | Build images using `--no-cache` flag |
| _ssl_      | Enable SSL support                   |

If you want to use your own data, please provide the following files into `api/data` directory<sup>2</sup>:

- Tag embeddings such as music genres are expected through `embeddings.csv` CSV file.
- Reduced embeddings for display are expected through `embeddings_reduced.csv` CSV file.
- Supported language are expected through `languages.csv` CSV file.
- Indexed entities are expected through `entites.csv` CSV file.
- Test corpus is expected through `corpus.csv` CSV file.

> <sup>2</sup> you need to clean the data storage and index to force data ingestion when you redeploy.

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
