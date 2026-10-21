# LaunchPilot — kit de démarrage

Copilote d'agents qui anticipe les ruptures d'un lancement cosmétique (marque fictive Maison Aurore, données 100 % synthétiques).

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `schema.sql` | Schéma PostgreSQL : données de base, transactions, flux, mémoire (`supplier_reliability`), sorties d'agents, traces |
| `generate_data.py` | Génère `data/` : CSV, `events.jsonl` (20 perturbations + 15 bruits), `ground_truth.json` |
| `projection.py` | Moteur déterministe que les agents appellent : modes `naive` et `learned` (mémoire fournisseur, délai prudent = moyenne + 1 écart-type) |
| `evaluate.py` | Rejoue le flux et compare baseline vs mémoire → `data/evaluation.json` |
| `load_to_postgres.py` | Crée le schéma et charge les CSV dans Aiven PostgreSQL |
| `replay_events.py` | Rejoue le flux en "live" (table `events`, + Kafka si configuré) |
| `app.py`, `Dockerfile`, `docker-compose.yml` | Squelette pour valider le déploiement Aiven Runtime ce soir |

## Démarrage

```bash
pip install -r requirements.txt
python generate_data.py              # seed 42 par défaut
python evaluate.py                   # baseline 1/4 vs mémoire 4/4
export DATABASE_URL="postgres://avnadmin:...@...aivencloud.com:PORT/defaultdb?sslmode=require"
python load_to_postgres.py --reset
python replay_events.py --speed 2 --until EV-019
```

## Résultats de référence (scénario enregistré, données synthétiques)

- Seed 42 : baseline 1/4 ruptures détectées, mémoire apprise 4/4, 0 fausse alerte. Pompe vue 39 jours avant la rupture (S46, semaine du lancement), invisible pour la baseline.
- 11 tirages (seeds 1–10 + 42) : 37/44 (84 %) contre 11/44 (25 %), 0 fausse alerte dans les deux cas.
