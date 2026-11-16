"""PKT Train as a module of PK Transport (plugin API 1, see PK-Transport/pkt/plugin.py).

Light at the top: PK Transport imports this file on its Home page for summary() / recent(); the heavy page code is imported in create()."""
import os

API = 1


def texts():
    from pkt_train.texts import TEXTS
    return TEXTS


def _runs(app):
    from pkt_train import runs
    return runs.find_runs(os.path.join(app.user_data_dir("PKT-Train"), "Runs"))


def summary(app, folder):
    runs = _runs(app)
    if not runs:
        return app.t("home_train_none")
    best = max((r["map50_95"] for r in runs if r["map50_95"] is not None), default=None)
    text = app.t("home_train_runs", n=len(runs))
    if best is not None:
        text += " \u00b7 " + app.t("home_best_map", m=f"{best:.3f}")
    return text


def recent(app, folder):
    return [{"mtime": r["mtime"], "glyph": "\u25c8", "title": app.t("home_recent_run", run=r["run"], model=r["model"] or r["family"]),
             "meta": f"mAP50-95 {r['map50_95']:.3f}" if r["map50_95"] is not None else ""} for r in _runs(app)[:5]]


def create(parent, app, folder):
    from pkt_train.page import TrainPage
    return TrainPage(parent, app, folder)
