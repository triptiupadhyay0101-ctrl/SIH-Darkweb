from fastapi import APIRouter
from sqlalchemy import text
import joblib
import numpy as np

from app.database.neo4j_connection import driver
from app.database.connection import engine
from scipy.sparse import hstack


router = APIRouter()


# ============================================================
# LOAD STYLOMETRY MODEL
# ============================================================

stylometry_model = joblib.load("stylometry_model.joblib")
word_vectorizer = joblib.load("word_vectorizer.pkl")
char_vectorizer = joblib.load("char_vectorizer.pkl")



# ============================================================
# THREAT MODELS
# ============================================================

from pydantic import BaseModel


class ThreatCreate(BaseModel):
    title: str
    description: str
    source: str
    threat_type: str
    severity: str
    url: str


# ============================================================
# HEALTH
# ============================================================

@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# ============================================================
# THREATS
# ============================================================

@router.get("/threats")
def get_threats():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       title,
                       description,
                       source,
                       threat_type,
                       severity,
                       url,
                       created_at
                FROM threats
                ORDER BY id
            """)
        )

        threats = [
            dict(row._mapping)
            for row in result
        ]

    return threats


@router.post("/threats")
def create_threat(threat: ThreatCreate):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO threats
                (
                    title,
                    description,
                    source,
                    threat_type,
                    severity,
                    url
                )
                VALUES
                (
                    :title,
                    :description,
                    :source,
                    :threat_type,
                    :severity,
                    :url
                )
                RETURNING id,
                          title,
                          description,
                          source,
                          threat_type,
                          severity,
                          url,
                          created_at
            """),
            {
                "title": threat.title,
                "description": threat.description,
                "source": threat.source,
                "threat_type": threat.threat_type,
                "severity": threat.severity,
                "url": threat.url
            }
        )

        new_threat = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_threat


@router.get("/threats/search")
def search_threats(
    severity: str | None = None,
    threat_type: str | None = None
):

    query = """
        SELECT id,
               title,
               description,
               source,
               threat_type,
               severity,
               url,
               created_at
        FROM threats
        WHERE 1=1
    """

    params = {}

    if severity:

        query += " AND severity = :severity"

        params["severity"] = severity

    if threat_type:

        query += " AND threat_type = :threat_type"

        params["threat_type"] = threat_type

    query += " ORDER BY id"

    with engine.connect() as connection:

        result = connection.execute(
            text(query),
            params
        )

        threats = [
            dict(row._mapping)
            for row in result
        ]

    return threats


@router.get("/threats/{threat_id}")
def get_threat(threat_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       title,
                       description,
                       source,
                       threat_type,
                       severity,
                       url,
                       created_at
                FROM threats
                WHERE id = :threat_id
            """),
            {
                "threat_id": threat_id
            }
        )

        threat = result.fetchone()

    if threat is None:

        return {
            "error": "Threat not found"
        }

    return dict(threat._mapping)


# ============================================================
# ACTORS
# ============================================================

class ActorCreate(BaseModel):
    name: str
    category: str
    attribution_confidence: float
    source: str


@router.post("/actors")
def create_actor(actor: ActorCreate):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO actors
                (
                    name,
                    category,
                    attribution_confidence,
                    source
                )
                VALUES
                (
                    :name,
                    :category,
                    :attribution_confidence,
                    :source
                )
                RETURNING id,
                          name,
                          category,
                          attribution_confidence,
                          last_seen,
                          source,
                          created_at
            """),
            {
                "name": actor.name,
                "category": actor.category,
                "attribution_confidence":
                    actor.attribution_confidence,
                "source": actor.source
            }
        )

        new_actor = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_actor


@router.get("/actors")
def get_actors():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       name,
                       category,
                       attribution_confidence,
                       last_seen,
                       source,
                       created_at
                FROM actors
                ORDER BY id
            """)
        )

        actors = [
            dict(row._mapping)
            for row in result
        ]

    return actors


# ============================================================
# ACTOR HANDLES
# ============================================================

class HandleCreate(BaseModel):
    actor_id: int
    handle: str
    platform: str
    source: str


@router.post("/actor-handles")
def create_handle(handle: HandleCreate):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO actor_handles
                (
                    actor_id,
                    handle,
                    platform,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :handle,
                    :platform,
                    :source
                )
                RETURNING id,
                          actor_id,
                          handle,
                          platform,
                          source,
                          created_at
            """),
            {
                "actor_id": handle.actor_id,
                "handle": handle.handle,
                "platform": handle.platform,
                "source": handle.source
            }
        )

        new_handle = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_handle


@router.get("/actor-handles")
def get_actor_handles():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       handle,
                       platform,
                       source,
                       created_at
                FROM actor_handles
                ORDER BY id
            """)
        )

        handles = [
            dict(row._mapping)
            for row in result
        ]

    return handles


# ============================================================
# PGP KEYS
# ============================================================

class PGPKeyCreate(BaseModel):
    actor_id: int
    fingerprint: str
    key_id: str
    source: str


@router.post("/pgp-keys")
def create_pgp_key(key: PGPKeyCreate):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO pgp_keys
                (
                    actor_id,
                    fingerprint,
                    key_id,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :fingerprint,
                    :key_id,
                    :source
                )
                RETURNING id,
                          actor_id,
                          fingerprint,
                          key_id,
                          source,
                          created_at
            """),
            {
                "actor_id": key.actor_id,
                "fingerprint": key.fingerprint,
                "key_id": key.key_id,
                "source": key.source
            }
        )

        new_key = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_key


@router.get("/pgp-keys")
def get_pgp_keys():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       fingerprint,
                       key_id,
                       source,
                       created_at
                FROM pgp_keys
                ORDER BY id
            """)
        )

        keys = [
            dict(row._mapping)
            for row in result
        ]

    return keys


# ============================================================
# WALLETS
# ============================================================

class WalletCreate(BaseModel):
    actor_id: int
    wallet_address: str
    blockchain: str
    source: str


@router.post("/wallets")
def create_wallet(wallet: WalletCreate):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO wallets
                (
                    actor_id,
                    wallet_address,
                    blockchain,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :wallet_address,
                    :blockchain,
                    :source
                )
                RETURNING id,
                          actor_id,
                          wallet_address,
                          blockchain,
                          source,
                          created_at
            """),
            {
                "actor_id": wallet.actor_id,
                "wallet_address":
                    wallet.wallet_address,
                "blockchain": wallet.blockchain,
                "source": wallet.source
            }
        )

        new_wallet = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_wallet


@router.get("/wallets")
def get_wallets():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       wallet_address,
                       blockchain,
                       source,
                       created_at
                FROM wallets
                ORDER BY id
            """)
        )

        wallets = [
            dict(row._mapping)
            for row in result
        ]

    return wallets


# ============================================================
# ACTOR RELATIONSHIPS
# ============================================================

class RelationshipCreate(BaseModel):
    actor_id: int
    related_actor_id: int
    relationship_type: str
    confidence: float
    source: str


@router.post("/actor-relationships")
def create_relationship(
    relationship: RelationshipCreate
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO actor_relationships
                (
                    actor_id,
                    related_actor_id,
                    relationship_type,
                    confidence,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :related_actor_id,
                    :relationship_type,
                    :confidence,
                    :source
                )
                RETURNING id,
                          actor_id,
                          related_actor_id,
                          relationship_type,
                          confidence,
                          source,
                          created_at
            """),
            {
                "actor_id":
                    relationship.actor_id,
                "related_actor_id":
                    relationship.related_actor_id,
                "relationship_type":
                    relationship.relationship_type,
                "confidence":
                    relationship.confidence,
                "source":
                    relationship.source
            }
        )

        new_relationship = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_relationship


@router.get("/actor-relationships")
def get_relationships():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       related_actor_id,
                       relationship_type,
                       confidence,
                       source,
                       created_at
                FROM actor_relationships
                ORDER BY id
            """)
        )

        relationships = [
            dict(row._mapping)
            for row in result
        ]

    return relationships
# ============================================================
# NEO4J ACTOR RELATIONSHIP SYNC
# ============================================================

@router.post("/neo4j/relationships/{actor_id}")
def sync_relationships_to_neo4j(actor_id: int):

    with engine.connect() as connection:

        relationships = connection.execute(
            text("""
                SELECT
                    actor_id,
                    related_actor_id,
                    relationship_type,
                    confidence,
                    source
                FROM actor_relationships
                WHERE actor_id = :actor_id
                   OR related_actor_id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    if not relationships:
        return {
            "message": "No actor relationships found",
            "actor_id": actor_id,
            "count": 0
        }

    with driver.session(database="sih-darkweb") as session:

        for relationship in relationships:

            confidence = relationship["confidence"]

            if confidence is not None:
                confidence = float(confidence)

            relationship_type = str(
                relationship["relationship_type"]
            ).upper().replace(" ", "_")

            session.run(
                """
                MATCH (a:Actor {id: $actor_id})
                MATCH (b:Actor {id: $related_actor_id})

                MERGE (a)-[r:RELATED_TO {
                    type: $relationship_type
                }]->(b)

                SET r.confidence = $confidence,
                    r.source = $source
                """,
                actor_id=int(relationship["actor_id"]),
                related_actor_id=int(
                    relationship["related_actor_id"]
                ),
                relationship_type=relationship_type,
                confidence=confidence,
                source=str(relationship["source"])
                if relationship["source"] else None
            )

    return {
        "message": "Actor relationships synced to Neo4j",
        "actor_id": actor_id,
        "count": len(relationships)
    }

# ============================================================
# INFRASTRUCTURE
# ============================================================

class InfrastructureCreate(BaseModel):
    actor_id: int
    indicator: str
    indicator_type: str
    value: str
    source: str
    confidence: float


@router.post("/infrastructure")
def create_infrastructure(
    item: InfrastructureCreate
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO infrastructure
                (
                    actor_id,
                    indicator,
                    indicator_type,
                    value,
                    source,
                    confidence
                )
                VALUES
                (
                    :actor_id,
                    :indicator,
                    :indicator_type,
                    :value,
                    :source,
                    :confidence
                )
                RETURNING id,
                          actor_id,
                          indicator,
                          indicator_type,
                          value,
                          source,
                          confidence,
                          created_at
            """),
            {
                "actor_id": item.actor_id,
                "indicator": item.indicator,
                "indicator_type":
                    item.indicator_type,
                "value": item.value,
                "source": item.source,
                "confidence":
                    item.confidence
            }
        )

        new_item = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_item


@router.get("/infrastructure")
def get_infrastructure():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       indicator,
                       indicator_type,
                       value,
                       source,
                       confidence,
                       created_at
                FROM infrastructure
                ORDER BY id
            """)
        )

        infrastructure = [
            dict(row._mapping)
            for row in result
        ]

    return infrastructure
# ============================================================
# INFRASTRUCTURE ANALYSIS
# ============================================================

@router.get("/infrastructure/analyze/{actor_id}")
def analyze_infrastructure(actor_id: int):

    with engine.connect() as connection:

        indicators = connection.execute(
            text("""
                SELECT
                    id,
                    indicator,
                    indicator_type,
                    value,
                    source,
                    confidence
                FROM infrastructure
                WHERE actor_id = :actor_id
                ORDER BY id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    findings = []

    for item in indicators:

        indicator_type = (
            str(item["indicator_type"]).lower()
            if item["indicator_type"]
            else ""
        )

        value = (
            str(item["value"])
            if item["value"]
            else ""
        )

        confidence = item["confidence"]

        if confidence is not None:
            confidence = float(confidence)
        else:
            confidence = 0.0

        detection = "Normal"

        # Check for common infrastructure clues
        if indicator_type in [
            "server",
            "server-status",
            "ssl",
            "certificate",
            "banner",
            "domain",
            "descriptor"
        ]:
            detection = "Potential Infrastructure Clue"

        findings.append({
            "infrastructure_id": item["id"],
            "indicator": item["indicator"],
            "indicator_type": item["indicator_type"],
            "value": value,
            "source": item["source"],
            "confidence": confidence,
            "detection": detection
        })

    return {
        "actor_id": actor_id,
        "total_indicators": len(findings),
        "findings": findings
    }

# ============================================================
# EVIDENCE
# ============================================================

class EvidenceCreate(BaseModel):
    actor_id: int
    evidence_type: str
    description: str
    source: str
    reference: str
    confidence: float


@router.post("/evidence")
def create_evidence(
    evidence: EvidenceCreate
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO evidence
                (
                    actor_id,
                    evidence_type,
                    description,
                    source,
                    reference,
                    confidence
                )
                VALUES
                (
                    :actor_id,
                    :evidence_type,
                    :description,
                    :source,
                    :reference,
                    :confidence
                )
                RETURNING id,
                          actor_id,
                          evidence_type,
                          description,
                          source,
                          reference,
                          confidence,
                          created_at
            """),
            {
                "actor_id": evidence.actor_id,
                "evidence_type":
                    evidence.evidence_type,
                "description":
                    evidence.description,
                "source": evidence.source,
                "reference":
                    evidence.reference,
                "confidence":
                    evidence.confidence
            }
        )

        new_evidence = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_evidence


@router.get("/evidence")
def get_evidence():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       evidence_type,
                       description,
                       source,
                       reference,
                       confidence,
                       created_at
                FROM evidence
                ORDER BY id
            """)
        )

        evidence = [
            dict(row._mapping)
            for row in result
        ]

    return evidence


# ============================================================
# BITCOIN ENTITIES
# ============================================================

@router.get("/bitcoin-entities")
def get_bitcoin_entities():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT record_id,
                       total_inflow_btc,
                       total_outflow_btc,
                       avg_tx_value,
                       tx_count_in,
                       tx_count_out,
                       active_duration_days,
                       in_out_ratio,
                       temporal_entropy,
                       address_count,
                       entity_label
                FROM bitcoin_entities
                ORDER BY record_id
                LIMIT 100
            """)
        )

        entities = [
            dict(row._mapping)
            for row in result
        ]

    return entities


# ============================================================
# INTELLIGENCE SEARCH
# ============================================================

@router.get("/intelligence/search")
def intelligence_search(q: str):

    results = []

    with engine.connect() as connection:

        # ----------------------------
        # Actors
        # ----------------------------

        actor_result = connection.execute(
            text("""
                SELECT id,
                       name,
                       category,
                       attribution_confidence,
                       source
                FROM actors
                WHERE name ILIKE :q
            """),
            {
                "q": f"%{q}%"
            }
        )

        for row in actor_result:

            results.append(
                {
                    "type": "actor",
                    "data": dict(row._mapping)
                }
            )

        # ----------------------------
        # Handles
        # ----------------------------

        handle_result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       handle,
                       platform,
                       source
                FROM actor_handles
                WHERE handle ILIKE :q
            """),
            {
                "q": f"%{q}%"
            }
        )

        for row in handle_result:

            results.append(
                {
                    "type": "handle",
                    "data": dict(row._mapping)
                }
            )

        # ----------------------------
        # PGP
        # ----------------------------

        pgp_result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       fingerprint,
                       key_id,
                       source
                FROM pgp_keys
                WHERE fingerprint ILIKE :q
                   OR key_id ILIKE :q
            """),
            {
                "q": f"%{q}%"
            }
        )

        for row in pgp_result:

            results.append(
                {
                    "type": "pgp_key",
                    "data": dict(row._mapping)
                }
            )

        # ----------------------------
        # Bitcoin
        # ----------------------------

        bitcoin_result = connection.execute(
            text("""
                SELECT record_id,
                       address_count,
                       entity_label
                FROM bitcoin_entities
                WHERE CAST(record_id AS TEXT) ILIKE :q
                   OR CAST(entity_label AS TEXT) ILIKE :q
            """),
            {
                "q": f"%{q}%"
            }
        )

        for row in bitcoin_result:

            results.append(
                {
                    "type": "bitcoin_entity",
                    "data": dict(row._mapping)
                }
            )

    return {
        "query": q,
        "results": results
    }


# ============================================================
# TIMELINE
# ============================================================

class TimelineEventCreate(BaseModel):
    actor_id: int
    event_type: str
    description: str
    source: str
    event_time: str
    confidence: float


@router.post("/timeline")
def create_timeline_event(
    event: TimelineEventCreate
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO timeline_events
                (
                    actor_id,
                    event_type,
                    description,
                    source,
                    event_time,
                    confidence
                )
                VALUES
                (
                    :actor_id,
                    :event_type,
                    :description,
                    :source,
                    :event_time,
                    :confidence
                )
                RETURNING id,
                          actor_id,
                          event_type,
                          description,
                          source,
                          event_time,
                          confidence,
                          created_at
            """),
            {
                "actor_id": event.actor_id,
                "event_type": event.event_type,
                "description": event.description,
                "source": event.source,
                "event_time": event.event_time,
                "confidence": event.confidence
            }
        )

        new_event = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_event


@router.get("/timeline/{actor_id}")
def get_actor_timeline(actor_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       event_type,
                       description,
                       source,
                       event_time,
                       confidence,
                       created_at
                FROM timeline_events
                WHERE actor_id = :actor_id
                ORDER BY event_time
            """),
            {
                "actor_id": actor_id
            }
        )

        events = [
            dict(row._mapping)
            for row in result
        ]

    return events
# ============================================================
# AUTOMATIC INFRASTRUCTURE TIMELINE
# ============================================================

@router.post("/timeline/infrastructure/{actor_id}")
def add_infrastructure_to_timeline(actor_id: int):

    with engine.connect() as connection:

        indicators = connection.execute(
            text("""
                SELECT
                    indicator,
                    indicator_type,
                    value,
                    source,
                    confidence,
                    created_at
                FROM infrastructure
                WHERE actor_id = :actor_id
                ORDER BY created_at
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        if not indicators:
            return {
                "message": "No infrastructure indicators found",
                "actor_id": actor_id,
                "events_created": 0
            }

        events_created = 0

        for item in indicators:

            description = (
                f"Infrastructure indicator detected: "
                f"{item['indicator']} = {item['value']}"
            )

            connection.execute(
                text("""
                    INSERT INTO timeline_events
                    (
                        actor_id,
                        event_type,
                        description,
                        source,
                        event_time,
                        confidence
                    )
                    VALUES
                    (
                        :actor_id,
                        :event_type,
                        :description,
                        :source,
                        :event_time,
                        :confidence
                    )
                """),
                {
                    "actor_id": actor_id,
                    "event_type": "Infrastructure Detection",
                    "description": description,
                    "source": item["source"] or "Infrastructure Analyzer",
                    "event_time": item["created_at"],
                    "confidence": float(item["confidence"])
                    if item["confidence"] is not None else 0.0
                }
            )

            events_created += 1

        connection.commit()

    return {
        "message": "Infrastructure findings added to timeline",
        "actor_id": actor_id,
        "events_created": events_created
    }


# ============================================================
# STYLOMETRY
# ============================================================

class StylometryCreate(BaseModel):
    actor_id: int
    compared_text: str
    similarity_score: float
    model: str
    source: str


# ------------------------------------------------------------
# PREDICT
# IMPORTANT: This route comes BEFORE /stylometry/{actor_id}
# ------------------------------------------------------------

@router.post("/stylometry/predict")
def predict_stylometry(text: str):
    word_features = word_vectorizer.transform([text])
    char_features = char_vectorizer.transform([text])

    features = hstack([
        word_features,
        char_features
    ])

    prediction = stylometry_model.predict(features)

    decision_scores = np.asarray(
        stylometry_model.decision_function(features)
    ).ravel()

    exp_scores = np.exp(
        decision_scores - decision_scores.max()
    )

    relative_confidence = (
        exp_scores.max() / exp_scores.sum()
    )

    match_score = relative_confidence * 100

    return {
        "predicted_author": prediction[0].item(),
        "match_score": round(float(match_score), 2)
    }
# # MODEL 2 - TUNED NAIVE BAYES

    features = model2_vectorizer.transform([text])

    prediction = model2.predict(features)

    probabilities = model2.predict_proba(features)[0]

    confidence = float(probabilities.max() * 100)

    return {
        "predicted_author": int(prediction[0]),
        "match_score": round(confidence, 2)
    }
# MODEL 2 - TUNED NAIVE BAYES
model2 = joblib.load("models/model2_tuned_alpha001.pkl")
model2_vectorizer = joblib.load(
    "models/model2_tuned_tfidf_vectorizer.pkl"
)


@router.post("/stylometry/model2")
def predict_stylometry_model2(text: str):
    features = model2_vectorizer.transform([text])

    prediction = model2.predict(features)

    probabilities = model2.predict_proba(features)[0]

    confidence = float(probabilities.max() * 100)

    return {
        "predicted_author": int(prediction[0]),
        "match_score": round(confidence, 2)
    }
# MODEL 2 - TUNED NAIVE BAYES


# ---------# MODEL 2 - TUNED NAIVE BAYES
# ------------------------------------------------------------
# MODEL 3 - RANDOM FOREST
# ------------------------------------------------------------

model3 = joblib.load("model3_random_forest.pkl")
model3_features = joblib.load("model3_features.pkl")


def extract_model3_features(text):
    import re

    words = re.findall(r"\b\w+\b", text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]

    word_count = len(words)
    sentence_count = len(sentences)
    character_count = len(text)
    average_word_length = (
        sum(len(word) for word in words) / word_count
        if word_count else 0
    )
    average_sentence_length = (
        word_count / sentence_count
        if sentence_count else 0
    )
    punctuation_count = sum(
        1 for char in text if char in ".,!?;:'\"-()[]{}"
    )
    uppercase_count = sum(
        1 for char in text if char.isupper()
    )
    digit_count = sum(
        1 for char in text if char.isdigit()
    )
    unique_words = len(set(words))
    vocabulary_richness = (
        unique_words / word_count
        if word_count else 0
    )

    feature_values = {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "character_count": character_count,
        "average_word_length": average_word_length,
        "average_sentence_length": average_sentence_length,
        "punctuation_count": punctuation_count,
        "uppercase_count": uppercase_count,
        "digit_count": digit_count,
        "unique_words": unique_words,
        "vocabulary_richness": vocabulary_richness
    }

    return [
        feature_values[name]
        for name in model3_features
    ]


@router.post("/stylometry/model3")
def predict_stylometry_model3(text: str):
    features = np.array(
        [extract_model3_features(text)]
    )

    prediction = model3.predict(features)

    if hasattr(model3, "predict_proba"):
        probabilities = model3.predict_proba(features)[0]
        confidence = float(probabilities.max() * 100)
    else:
        confidence = 0.0

    return {
        "predicted_author": int(prediction[0]),
        "match_score": round(confidence, 2)
    }
# ------------------------------------------------------------
# SAVE STYLOMETRY RESULT
# ------------------------------------------------------------

@router.post("/stylometry/save")
def save_stylometry_result(
    actor_id: int,
    compared_text: str,
    similarity_score: float,
   source: str = "AI Stylometry"
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO stylometry_results
                (
                    actor_id,
                    compared_text,
                    similarity_score,
                    model,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :compared_text,
                    :similarity_score,
                    :model,
                    :source
                )
                RETURNING id,
                          actor_id,
                          compared_text,
                          similarity_score,
                          model,
                          source,
                          created_at
            """),
            {
                "actor_id": actor_id,
                "compared_text": compared_text,
                "similarity_score":
                    similarity_score,
                "model":
                    "TF-IDF + LinearSVC",
                "source": source
            }
        )

        saved_result = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return saved_result


# ------------------------------------------------------------
# EXISTING STYLOMETRY DATABASE ROUTES
# ------------------------------------------------------------

@router.post("/stylometry")
def create_stylometry_result(
    result_data: StylometryCreate
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO stylometry_results
                (
                    actor_id,
                    compared_text,
                    similarity_score,
                    model,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :compared_text,
                    :similarity_score,
                    :model,
                    :source
                )
                RETURNING id,
                          actor_id,
                          compared_text,
                          similarity_score,
                          model,
                          source,
                          created_at
            """),
            {
                "actor_id":
                    result_data.actor_id,
                "compared_text":
                    result_data.compared_text,
                "similarity_score":
                    result_data.similarity_score,
                "model":
                    result_data.model,
                "source":
                    result_data.source
            }
        )

        new_result = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_result


# IMPORTANT:
# This dynamic route is AFTER /stylometry/predict
# so "predict" will not be interpreted as an actor_id.

@router.get("/stylometry/{actor_id}")
def get_stylometry_results(actor_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       compared_text,
                       similarity_score,
                       model,
                       source,
                       created_at
                FROM stylometry_results
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {
                "actor_id": actor_id
            }
        )

        results = [
            dict(row._mapping)
            for row in result
        ]

    return results


# ============================================================
# BEHAVIORAL PROFILES
# ============================================================

class BehavioralProfileCreate(BaseModel):
    actor_id: int
    behavior_type: str
    behavior_data: str
    risk_score: float
    source: str


@router.post("/behavioral-profiles")
def create_behavioral_profile(
    profile: BehavioralProfileCreate
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO behavioral_profiles
                (
                    actor_id,
                    behavior_type,
                    behavior_data,
                    risk_score,
                    source
                )
                VALUES
                (
                    :actor_id,
                    :behavior_type,
                    :behavior_data,
                    :risk_score,
                    :source
                )
                RETURNING id,
                          actor_id,
                          behavior_type,
                          behavior_data,
                          risk_score,
                          source,
                          created_at
            """),
            {
                "actor_id": profile.actor_id,
                "behavior_type":
                    profile.behavior_type,
                "behavior_data":
                    profile.behavior_data,
                "risk_score":
                    profile.risk_score,
                "source":
                    profile.source
            }
        )

        new_profile = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return new_profile


@router.get("/behavioral-profiles/{actor_id}")
def get_behavioral_profile(actor_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       behavior_type,
                       behavior_data,
                       risk_score,
                       source,
                       created_at
                FROM behavioral_profiles
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {
                "actor_id": actor_id
            }
        )

        profiles = [
            dict(row._mapping)
            for row in result
        ]

    return profiles


# ============================================================
# BEHAVIORAL SCORES
# ============================================================

@router.get("/behavioral-scores")
def get_behavioral_scores():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       record_id,
                       entity_label,
                       behavior_score,
                       created_at
                FROM behavioral_scores
                ORDER BY record_id
                LIMIT 100
            """)
        )

        scores = [
            dict(row._mapping)
            for row in result
        ]

    return scores


# ============================================================
# ATTRIBUTION
# ============================================================

# ============================================================
# ATTRIBUTION
# ============================================================

class AttributionCreate(BaseModel):
    actor_id: int
    stylometry_score: float
    behavior_score: float
    evidence_score: float
    reasoning: str


@router.post("/attribution")
def create_attribution(
    result_data: AttributionCreate
):

    overall_confidence = (
        result_data.stylometry_score * 0.35
        + result_data.behavior_score * 0.35
        + result_data.evidence_score * 0.30
    )

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO attribution_results
                (
                    actor_id,
                    stylometry_score,
                    behavior_score,
                    evidence_score,
                    overall_confidence,
                    reasoning
                )
                VALUES
                (
                    :actor_id,
                    :stylometry_score,
                    :behavior_score,
                    :evidence_score,
                    :overall_confidence,
                    :reasoning
                )
                RETURNING id,
                          actor_id,
                          stylometry_score,
                          behavior_score,
                          evidence_score,
                          overall_confidence,
                          reasoning,
                          created_at
            """),
            {
                "actor_id": result_data.actor_id,
                "stylometry_score": result_data.stylometry_score,
                "behavior_score": result_data.behavior_score,
                "evidence_score": result_data.evidence_score,
                "overall_confidence": overall_confidence,
                "reasoning": result_data.reasoning
            }
        )

        attribution = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return attribution
@router.get("/attribution/{actor_id}")
def get_attribution(actor_id:int):


    with engine.connect() as connection:

        # Get latest stylometry score
        stylometry = connection.execute(
            text("""
                SELECT similarity_score
                FROM stylometry_results
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"actor_id": actor_id}
        ).scalar()

        # Get latest behavioral score
        behavior = connection.execute(
            text("""
                SELECT risk_score
                FROM behavioral_profiles
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"actor_id": actor_id}
        ).scalar()

        # Get latest evidence score
        evidence = connection.execute(
            text("""
                SELECT confidence
                FROM evidence
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"actor_id": actor_id}
        ).scalar()

    stylometry_score = float(stylometry) if stylometry is not None else 0.0
    behavior_score = float(behavior) if behavior is not None else 0.0
    evidence_score = float(evidence) if evidence is not None else 0.0

    overall_confidence = (
        stylometry_score * 0.35
        + behavior_score * 0.35
        + evidence_score * 0.30
    )

    reasoning = (
        "Automatic attribution calculated using "
        "stylometry (35%), behavioral analysis (35%), "
        "and supporting evidence (30%)."
    )

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO attribution_results
                (
                    actor_id,
                    stylometry_score,
                    behavior_score,
                    evidence_score,
                    overall_confidence,
                    reasoning
                )
                VALUES
                (
                    :actor_id,
                    :stylometry_score,
                    :behavior_score,
                    :evidence_score,
                    :overall_confidence,
                    :reasoning
                )
                RETURNING id,
                          actor_id,
                          stylometry_score,
                          behavior_score,
                          evidence_score,
                          overall_confidence,
                          reasoning,
                          created_at
            """),
            {
                "actor_id": actor_id,
                "stylometry_score": stylometry_score,
                "behavior_score": behavior_score,
                "evidence_score": evidence_score,
                "overall_confidence": overall_confidence,
                "reasoning": reasoning
            }
        )

        attribution = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return attribution

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       stylometry_score,
                       behavior_score,
                       evidence_score,
                       overall_confidence,
                       reasoning,
                       created_at
                FROM attribution_results
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {
                "actor_id": actor_id
            }
        )

        results = [
            dict(row._mapping)
            for row in result
        ]

    return results
# ============================================================
# AUTOMATIC ATTRIBUTION
# ============================================================

@router.post("/attribution/auto/{actor_id}")
def automatic_attribution(actor_id: int):

    with engine.connect() as connection:

        # Get latest stylometry score
        stylometry = connection.execute(
            text("""
                SELECT similarity_score
                FROM stylometry_results
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"actor_id": actor_id}
        ).scalar()

        # Get latest behavioral score
        behavior = connection.execute(
            text("""
                SELECT risk_score
                FROM behavioral_profiles
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"actor_id": actor_id}
        ).scalar()

        # Get latest evidence score
        evidence = connection.execute(
            text("""
                SELECT confidence
                FROM evidence
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"actor_id": actor_id}
        ).scalar()

    # Use 0 when a score is not available
    stylometry_score = float(stylometry) if stylometry is not None else 0.0
    behavior_score = float(behavior) if behavior is not None else 0.0
    evidence_score = float(evidence) if evidence is not None else 0.0

    # Calculate overall confidence
    overall_confidence = (
        stylometry_score * 0.35
        + behavior_score * 0.35
        + evidence_score * 0.30
    )

    reasoning = (
        "Automatic attribution calculated using "
        "stylometry (35%), behavioral analysis (35%), "
        "and evidence confidence (30%)."
    )

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                INSERT INTO attribution_results
                (
                    actor_id,
                    stylometry_score,
                    behavior_score,
                    evidence_score,
                    overall_confidence,
                    reasoning
                )
                VALUES
                (
                    :actor_id,
                    :stylometry_score,
                    :behavior_score,
                    :evidence_score,
                    :overall_confidence,
                    :reasoning
                )
                RETURNING id,
                          actor_id,
                          stylometry_score,
                          behavior_score,
                          evidence_score,
                          overall_confidence,
                          reasoning,
                          created_at
            """),
            {
                "actor_id": actor_id,
                "stylometry_score": stylometry_score,
                "behavior_score": behavior_score,
                "evidence_score": evidence_score,
                "overall_confidence": overall_confidence,
                "reasoning": reasoning
            }
        )

        attribution = dict(
            result.fetchone()._mapping
        )

        connection.commit()

    return attribution


# ============================================================
# ACTOR GRAPH
# ============================================================

@router.get("/graph/actor/{actor_id}")
def get_actor_graph(actor_id: int):

    with engine.connect() as connection:

        # Actor
        actor = connection.execute(
            text("""
                SELECT id,
                       name,
                       category,
                       attribution_confidence,
                       source
                FROM actors
                WHERE id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        ).fetchone()

        if actor is None:

            return {
                "error": "Actor not found"
            }

        # Handles
        handles = connection.execute(
            text("""
                SELECT id,
                       handle,
                       platform,
                       source
                FROM actor_handles
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        # PGP keys
        pgp_keys = connection.execute(
            text("""
                SELECT id,
                       fingerprint,
                       key_id,
                       source
                FROM pgp_keys
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        # Wallets
        wallets = connection.execute(
            text("""
                SELECT id,
                       wallet_address,
                       blockchain,
                       source
                FROM wallets
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        # Infrastructure
        infrastructure = connection.execute(
            text("""
                SELECT id,
                       indicator,
                       indicator_type,
                       value,
                       source,
                       confidence
                FROM infrastructure
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        # Relationships
        relationships = connection.execute(
            text("""
                SELECT id,
                       actor_id,
                       related_actor_id,
                       relationship_type,
                       confidence,
                       source
                FROM actor_relationships
                WHERE actor_id = :actor_id
                   OR related_actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        return {
            "actor":
                dict(actor._mapping),

            "handles":
                [
                    dict(row._mapping)
                    for row in handles
                ],

            "pgp_keys":
                [
                    dict(row._mapping)
                    for row in pgp_keys
                ],

            "wallets":
                [
                    dict(row._mapping)
                    for row in wallets
                ],

            "infrastructure":
                [
                    dict(row._mapping)
                    for row in infrastructure
                ],

            "relationships":
                [
                    dict(row._mapping)
                    for row in relationships
                ]
        }


# ============================================================
# EXPORT ACTOR
# ============================================================

@router.get("/export/actor/{actor_id}")
def export_actor(actor_id: int):

    with engine.connect() as connection:

        actor = connection.execute(
            text("""
                SELECT id,
                       name,
                       category,
                       attribution_confidence,
                       source,
                       created_at
                FROM actors
                WHERE id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        ).fetchone()

        if actor is None:

            return {
                "error": "Actor not found"
            }

        data = {
            "actor":
                dict(actor._mapping)
        }

        # Handles
        handles = connection.execute(
            text("""
                SELECT id,
                       handle,
                       platform,
                       source,
                       created_at
                FROM actor_handles
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        data["handles"] = [
            dict(row._mapping)
            for row in handles
        ]

        # PGP keys
        pgp = connection.execute(
            text("""
                SELECT id,
                       fingerprint,
                       key_id,
                       source,
                       created_at
                FROM pgp_keys
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        data["pgp_keys"] = [
            dict(row._mapping)
            for row in pgp
        ]

        # Wallets
        wallets = connection.execute(
            text("""
                SELECT id,
                       wallet_address,
                       blockchain,
                       source,
                       created_at
                FROM wallets
                WHERE actor_id = :actor_id
            """),
            {
                "actor_id": actor_id
            }
        )

        data["wallets"] = [
            dict(row._mapping)
            for row in wallets
        ]

        return data
@router.get("/neo4j/test") 
def neo4j_test():
    with driver.session(database="sih-darkweb") as session:
        result = session.run(
            'RETURN "FastAPI → Neo4j connection successful" AS message'
        )
        return {"message": result.single()["message"]}
@router.post("/neo4j/actor/{actor_id}")
def sync_actor_to_neo4j(actor_id: int):

    with engine.connect() as connection:
        actor = connection.execute(
            text("""
                SELECT id, name, category, attribution_confidence, source
                FROM actors
                WHERE id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().first()

    if not actor:
        return {"error": "Actor not found"}

    confidence = actor["attribution_confidence"]

    if confidence is not None:
        confidence = float(confidence)

    actor_id_value = int(actor["id"])
    name_value = str(actor["name"])
    category_value = str(actor["category"]) if actor["category"] is not None else None
    source_value = str(actor["source"]) if actor["source"] is not None else None

    with driver.session(database="sih-darkweb") as session:
        session.run(
            """
            MERGE (a:Actor {id: $id})
            SET a.name = $name,
                a.category = $category,
                a.attribution_confidence = $confidence,
                a.source = $source
            """,
            id=actor_id_value,
            name=name_value,
            category=category_value,
            confidence=confidence,
            source=source_value
        )

    return {
        "message": "Actor synced to Neo4j",
        "actor_id": actor_id_value,
        "name": name_value
    }
@router.post("/neo4j/handles/{actor_id}")
def sync_handles_to_neo4j(actor_id: int):

    with engine.connect() as connection:
        handles = connection.execute(
            text("""
                SELECT handle, platform, source
                FROM actor_handles
                WHERE actor_id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    if not handles:
        return {"message": "No handles found", "actor_id": actor_id}

    with driver.session(database="sih-darkweb") as session:
        for handle in handles:
            session.run(
                """
                MATCH (a:Actor {id: $actor_id})
                MERGE (h:Handle {
                    handle: $handle,
                    platform: $platform
                })
                SET h.source = $source
                MERGE (a)-[:USES_HANDLE]->(h)
                """,
                actor_id=int(actor_id),
                handle=str(handle["handle"]),
                platform=str(handle["platform"]) if handle["platform"] else None,
                source=str(handle["source"]) if handle["source"] else None
            )

    return {
        "message": "Handles synced to Neo4j",
        "actor_id": actor_id,
        "count": len(handles)
    }
@router.post("/neo4j/pgp-keys/{actor_id}")
def sync_pgp_keys_to_neo4j(actor_id: int):

    with engine.connect() as connection:
        keys = connection.execute(
            text("""
                SELECT fingerprint, key_id, source
                FROM pgp_keys
                WHERE actor_id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    if not keys:
        return {"message": "No PGP keys found", "actor_id": actor_id}

    with driver.session(database="sih-darkweb") as session:
        for key in keys:
            session.run(
                """
                MATCH (a:Actor {id: $actor_id})
                MERGE (p:PGPKey {
                    fingerprint: $fingerprint
                })
                SET p.key_id = $key_id,
                    p.source = $source
                MERGE (a)-[:USES_PGP_KEY]->(p)
                """,
                actor_id=int(actor_id),
                fingerprint=str(key["fingerprint"]),
                key_id=str(key["key_id"]) if key["key_id"] else None,
                source=str(key["source"]) if key["source"] else None
            )

    return {
        "message": "PGP keys synced to Neo4j",
        "actor_id": actor_id,
        "count": len(keys)
    }
@router.post("/neo4j/wallets/{actor_id}")
def sync_wallets_to_neo4j(actor_id: int):

    with engine.connect() as connection:
        wallets = connection.execute(
            text("""
                SELECT wallet_address, blockchain, source
                FROM wallets
                WHERE actor_id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    if not wallets:
        return {"message": "No wallets found", "actor_id": actor_id}

    with driver.session(database="sih-darkweb") as session:
        for wallet in wallets:
            session.run(
                """
                MATCH (a:Actor {id: $actor_id})
                MERGE (w:Wallet {
                    address: $address,
                    blockchain: $blockchain
                })
                SET w.source = $source
                MERGE (a)-[:USES_WALLET]->(w)
                """,
                actor_id=int(actor_id),
                address=str(wallet["wallet_address"]),
                blockchain=str(wallet["blockchain"]) if wallet["blockchain"] else "Bitcoin",
                source=str(wallet["source"]) if wallet["source"] else None
            )

    return {
        "message": "Wallets synced to Neo4j",
        "actor_id": actor_id,
        "count": len(wallets)
    }
@router.post("/neo4j/infrastructure/{actor_id}")
def sync_infrastructure_to_neo4j(actor_id: int):

    with engine.connect() as connection:
        indicators = connection.execute(
            text("""
                SELECT indicator, indicator_type, value, source, confidence
                FROM infrastructure
                WHERE actor_id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    if not indicators:
        return {
            "message": "No infrastructure indicators found",
            "actor_id": actor_id
        }

    with driver.session(database="sih-darkweb") as session:
        for item in indicators:
            confidence = item["confidence"]

            if confidence is not None:
                confidence = float(confidence)

            session.run(
                """
                MATCH (a:Actor {id: $actor_id})
                MERGE (i:Infrastructure {
                    indicator: $indicator,
                    value: $value
                })
                SET i.indicator_type = $indicator_type,
                    i.source = $source,
                    i.confidence = $confidence
                MERGE (a)-[:HAS_INFRASTRUCTURE]->(i)
                """,
                actor_id=int(actor_id),
                indicator=str(item["indicator"]),
                indicator_type=str(item["indicator_type"]),
                value=str(item["value"]),
                source=str(item["source"]) if item["source"] else None,
                confidence=confidence
            )

    return {
        "message": "Infrastructure synced to Neo4j",
        "actor_id": actor_id,
        "count": len(indicators)
    }
# ============================================================
# UNIFIED ACTOR INVESTIGATION
# ============================================================

@router.get("/investigation/{actor_id}")
def get_full_investigation(actor_id: int):

    with engine.connect() as connection:

        # ----------------------------------------------------
        # Actor
        # ----------------------------------------------------

        actor = connection.execute(
            text("""
                SELECT
                    id,
                    name,
                    category,
                    attribution_confidence,
                    last_seen,
                    source,
                    created_at
                FROM actors
                WHERE id = :actor_id
            """),
            {"actor_id": actor_id}
        ).mappings().first()

        if not actor:
            return {
                "error": "Actor not found"
            }

        # ----------------------------------------------------
        # Handles
        # ----------------------------------------------------

        handles = connection.execute(
            text("""
                SELECT
                    id,
                    handle,
                    platform,
                    source,
                    created_at
                FROM actor_handles
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # PGP Keys
        # ----------------------------------------------------

        pgp_keys = connection.execute(
            text("""
                SELECT
                    id,
                    fingerprint,
                    key_id,
                    source,
                    created_at
                FROM pgp_keys
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Wallets
        # ----------------------------------------------------

        wallets = connection.execute(
            text("""
                SELECT
                    id,
                    wallet_address,
                    blockchain,
                    source,
                    created_at
                FROM wallets
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Infrastructure
        # ----------------------------------------------------

        infrastructure = connection.execute(
            text("""
                SELECT
                    id,
                    indicator,
                    indicator_type,
                    value,
                    source,
                    confidence,
                    created_at
                FROM infrastructure
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        evidence = connection.execute(
            text("""
                SELECT
                    id,
                    evidence_type,
                    description,
                    source,
                    reference,
                    confidence,
                    created_at
                FROM evidence
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Timeline
        # ----------------------------------------------------

        timeline = connection.execute(
            text("""
                SELECT
                    id,
                    event_type,
                    description,
                    source,
                    event_time,
                    confidence,
                    created_at
                FROM timeline_events
                WHERE actor_id = :actor_id
                ORDER BY event_time DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Stylometry
        # ----------------------------------------------------

        stylometry = connection.execute(
            text("""
                SELECT
                    id,
                    similarity_score,
                    model,
                    source,
                    created_at
                FROM stylometry_results
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Behavioral Profiles
        # ----------------------------------------------------

        behavioral_profiles = connection.execute(
            text("""
                SELECT
                    id,
                    behavior_type,
                    behavior_data,
                    risk_score,
                    source,
                    created_at
                FROM behavioral_profiles
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Attribution
        # ----------------------------------------------------

        attribution = connection.execute(
            text("""
                SELECT
                    id,
                    stylometry_score,
                    behavior_score,
                    evidence_score,
                    overall_confidence,
                    reasoning,
                    created_at
                FROM attribution_results
                WHERE actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

        # ----------------------------------------------------
        # Actor Relationships
        # ----------------------------------------------------

        relationships = connection.execute(
            text("""
                SELECT
                    id,
                    actor_id,
                    related_actor_id,
                    relationship_type,
                    confidence,
                    source,
                    created_at
                FROM actor_relationships
                WHERE actor_id = :actor_id
                   OR related_actor_id = :actor_id
                ORDER BY created_at DESC
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    # --------------------------------------------------------
    # Convert database rows to JSON-friendly dictionaries
    # --------------------------------------------------------

    return {
        "actor": dict(actor),

        "handles": [
            dict(row)
            for row in handles
        ],

        "pgp_keys": [
            dict(row)
            for row in pgp_keys
        ],

        "wallets": [
            dict(row)
            for row in wallets
        ],

        "infrastructure": [
            dict(row)
            for row in infrastructure
        ],

        "evidence": [
            dict(row)
            for row in evidence
        ],

        "timeline": [
            dict(row)
            for row in timeline
        ],

        "stylometry": [
            dict(row)
            for row in stylometry
        ],

        "behavioral_profiles": [
            dict(row)
            for row in behavioral_profiles
        ],

        "attribution": [
            dict(row)
            for row in attribution
        ],

        "relationships": [
            dict(row)
            for row in relationships
        ]
    }
# ============================================================
# INFRASTRUCTURE MATCHING
# ============================================================

@router.get("/infrastructure/match/{actor_id}")
def match_infrastructure(actor_id: int):

    with engine.connect() as connection:

        indicators = connection.execute(
            text("""
                SELECT
                    id,
                    indicator,
                    indicator_type,
                    value,
                    source,
                    confidence
                FROM infrastructure
                WHERE actor_id = :actor_id
                ORDER BY id
            """),
            {"actor_id": actor_id}
        ).mappings().all()

    matches = []

    # Compare every infrastructure indicator with every other
    # indicator belonging to this actor.
    for i in range(len(indicators)):

        for j in range(i + 1, len(indicators)):

            first = indicators[i]
            second = indicators[j]

            first_value = (
                str(first["value"]).strip().lower()
                if first["value"] else ""
            )

            second_value = (
                str(second["value"]).strip().lower()
                if second["value"] else ""
            )

            if not first_value or not second_value:
                continue

            # Exact value match
            if first_value == second_value:

                confidence_values = [
                    float(first["confidence"])
                    if first["confidence"] is not None else 0.0,
                    float(second["confidence"])
                    if second["confidence"] is not None else 0.0
                ]

                match_confidence = sum(confidence_values) / 2

                matches.append({
                    "indicator_1": first["indicator"],
                    "indicator_1_type": first["indicator_type"],
                    "value_1": first["value"],

                    "indicator_2": second["indicator"],
                    "indicator_2_type": second["indicator_type"],
                    "value_2": second["value"],

                    "match_type": "Exact Value Match",
                    "confidence": round(match_confidence, 2)
                })

    return {
        "actor_id": actor_id,
        "total_indicators": len(indicators),
        "matches_found": len(matches),
        "matches": matches
    }
# ============================================================
# INVESTIGATOR SEARCH
# ============================================================

@router.get("/investigate/search")
def investigate_search(q: str):

    results = []

    search_term = f"%{q}%"

    with engine.connect() as connection:

        # Actors
        actors = connection.execute(
            text("""
                SELECT id, name, category,
                       attribution_confidence, source
                FROM actors
                WHERE name ILIKE :q
            """),
            {"q": search_term}
        ).mappings().all()

        for row in actors:
            results.append({
                "match_type": "Actor",
                "actor_id": row["id"],
                "data": dict(row)
            })

        # Handles
        handles = connection.execute(
            text("""
                SELECT actor_id, handle, platform, source
                FROM actor_handles
                WHERE handle ILIKE :q
            """),
            {"q": search_term}
        ).mappings().all()

        for row in handles:
            results.append({
                "match_type": "Handle",
                "actor_id": row["actor_id"],
                "data": dict(row)
            })

        # PGP keys
        pgp_keys = connection.execute(
            text("""
                SELECT actor_id, fingerprint, key_id, source
                FROM pgp_keys
                WHERE fingerprint ILIKE :q
                   OR key_id ILIKE :q
            """),
            {"q": search_term}
        ).mappings().all()

        for row in pgp_keys:
            results.append({
                "match_type": "PGP Key",
                "actor_id": row["actor_id"],
                "data": dict(row)
            })

        # Wallets
        wallets = connection.execute(
            text("""
                SELECT actor_id, wallet_address,
                       blockchain, source
                FROM wallets
                WHERE wallet_address ILIKE :q
            """),
            {"q": search_term}
        ).mappings().all()

        for row in wallets:
            results.append({
                "match_type": "Wallet",
                "actor_id": row["actor_id"],
                "data": dict(row)
            })

        # Infrastructure
        infrastructure = connection.execute(
            text("""
                SELECT actor_id, indicator,
                       indicator_type, value,
                       source, confidence
                FROM infrastructure
                WHERE indicator ILIKE :q
                   OR value ILIKE :q
            """),
            {"q": search_term}
        ).mappings().all()

        for row in infrastructure:
            results.append({
                "match_type": "Infrastructure",
                "actor_id": row["actor_id"],
                "data": dict(row)
            })

    return {
        "query": q,
        "total_matches": len(results),
        "results": results
    }
# ============================================================
# SEARCH AND OPEN FULL INVESTIGATION
# ============================================================

@router.get("/investigate/{q}")
def investigate(q: str):

    search_term = f"%{q}%"
    actor_id = None

    with engine.connect() as connection:

        # Search actor name
        actor = connection.execute(
            text("""
                SELECT id
                FROM actors
                WHERE name ILIKE :q
                LIMIT 1
            """),
            {"q": search_term}
        ).scalar()

        if actor:
            actor_id = int(actor)

        # Search handle
        if actor_id is None:
            actor = connection.execute(
                text("""
                    SELECT actor_id
                    FROM actor_handles
                    WHERE handle ILIKE :q
                    LIMIT 1
                """),
                {"q": search_term}
            ).scalar()

            if actor:
                actor_id = int(actor)

        # Search PGP fingerprint/key ID
        if actor_id is None:
            actor = connection.execute(
                text("""
                    SELECT actor_id
                    FROM pgp_keys
                    WHERE fingerprint ILIKE :q
                       OR key_id ILIKE :q
                    LIMIT 1
                """),
                {"q": search_term}
            ).scalar()

            if actor:
                actor_id = int(actor)

        # Search wallet
        if actor_id is None:
            actor = connection.execute(
                text("""
                    SELECT actor_id
                    FROM wallets
                    WHERE wallet_address ILIKE :q
                    LIMIT 1
                """),
                {"q": search_term}
            ).scalar()

            if actor:
                actor_id = int(actor)

        # Search infrastructure
        if actor_id is None:
            actor = connection.execute(
                text("""
                    SELECT actor_id
                    FROM infrastructure
                    WHERE indicator ILIKE :q
                       OR value ILIKE :q
                    LIMIT 1
                """),
                {"q": search_term}
            ).scalar()

            if actor:
                actor_id = int(actor)

    if actor_id is None:
        return {
            "query": q,
            "message": "No matching actor found"
        }

    # Reuse the complete investigation endpoint
    investigation = get_full_investigation(actor_id)

    return {
        "query": q,
        "matched_actor_id": actor_id,
        "investigation": investigation
    }
# ============================================================
# NEO4J INVESTIGATION GRAPH
# ============================================================

@router.get("/neo4j/investigation/{actor_id}")
def get_neo4j_investigation(actor_id: int):

    with driver.session(database="sih-darkweb") as session:

        result = session.run(
            """
            MATCH (a:Actor {id: $actor_id})
            OPTIONAL MATCH path = (a)-[*1..2]-(n)
            RETURN a, relationships(path) AS relationships, nodes(path) AS nodes
            """,
            actor_id=int(actor_id)
        )

        records = list(result)

    if not records:
        return {
            "actor_id": actor_id,
            "nodes": [],
            "relationships": []
        }

    nodes = {}
    relationships = {}

    for record in records:

        actor_node = record["a"]

        nodes[actor_node.element_id] = {
            "id": actor_node.element_id,
            "labels": list(actor_node.labels),
            "properties": dict(actor_node)
        }

        for node in record["nodes"] or []:
            nodes[node.element_id] = {
                "id": node.element_id,
                "labels": list(node.labels),
                "properties": dict(node)
            }

        for rel in record["relationships"] or []:
            relationships[rel.element_id] = {
                "id": rel.element_id,
                "type": rel.type,
                "start_node": rel.start_node.element_id,
                "end_node": rel.end_node.element_id,
                "properties": dict(rel)
            }

    return {
        "actor_id": actor_id,
        "nodes": list(nodes.values()),
        "relationships": list(relationships.values())
    }