# LaunchPilot — kit de démarrage

Copilote d'agents qui anticipe les ruptures d'un lancement cosmétique (marque fictive Maison Aurore, données 100 % synthétiques).

## L'application

`app.py` est l'interface de démo (Streamlit), avec 4 onglets : Lancement, Mémoire fournisseur, Preuve, Traces des agents.

- **Sans rien configurer**, elle tourne : données en mémoire, agents en mode règles.
- **Avec `DATABASE_URL`** (Service URI Aiven PostgreSQL), elle crée les tables et charge les données toute seule au premier lancement. Alertes, scénarios, décisions et traces sont stockés dans Aiven.
- **Avec `ANTHROPIC_API_KEY`**, les agents Veille et Arbitrage tournent avec Claude en direct (tool use). L'avance rapide reste en mode règles, sauf le dernier événement (EV-019), traité en live.
- Optionnel : `CLAUDE_MODEL` pour changer de modèle, `ANTHROPIC_BASE_URL` pour passer par une passerelle (AI Gateway Aiven).

Parcours de démo : Réinitialiser → Avance rapide jusqu'à EV-019 → l'alerte pompe passe en critique → Proposer des solutions → Choisir un scénario → onglets Mémoire et Preuve.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `app.py` | Interface de démo |
| `agents.py` | Agents Veille et Arbitrage (Claude live + version règles) |
| `tools.py` | Outils métier appelés par les agents : projection, mémoire fournisseur, chiffrage des scénarios |
| `store.py` | Stockage : Aiven PostgreSQL ou mémoire |
| `projection.py` | Moteur de projection déterministe (modes naïf et appris, simulations) |
| `schema.sql` | Schéma PostgreSQL |
| `generate_data.py` | Génère les données synthétiques dans `data/` |
| `evaluate.py` | Preuve : baseline naïve vs mémoire → `data/evaluation.json` |
| `load_to_postgres.py`, `replay_events.py` | Scripts optionnels (l'app fait déjà le chargement) |
| `Dockerfile`, `docker-compose.yml` | Déploiement Aiven Runtime |

## Résultats de référence (scénario enregistré, données synthétiques)

- Seed 42 : baseline 1/4 ruptures détectées, LaunchPilot 4/4, 0 fausse alerte. Pompe vue 39 jours avant la rupture (semaine du 09/11), invisible pour la baseline.
- 11 tirages : 37/44 (84 %) contre 11/44 (25 %).
- Arbitrage pompe au 01/10 : 742 k€ de CA à risque sans action ; meilleure option = commande urgente chez Dosage Riviera + allocation prioritaire au coffret (impact 194 k€).
