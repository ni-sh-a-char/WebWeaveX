/**
 * Converted from Python: core/extract/facades/knowledge_facade.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildDependencyLineage, buildExecutionFlow, buildFrameworkRelationships, buildRepositoryKnowledge, buildSemanticGraph, buildServiceRelationships, clusterSemanticGraph, reasonOverSemanticGraph } from "../../knowledge/index.js";
import { resolveEntities } from "../../knowledge/reconstruction/entityResolutionEngine.js";
import { buildConceptGraph } from "../../knowledge/reconstruction/conceptGraphEngine.js";
import { buildSemanticRelationships as buildKnowledgeRelationshipsV2 } from "../../knowledge/semanticRelationshipV2Engine.js";
import { buildRepositoryKnowledgeV2 } from "../../knowledge/repositoryKnowledgeV2Engine.js";
import { buildDocumentKnowledgeV2 } from "../../knowledge/documentKnowledgeV2Engine.js";
import { buildInternetKnowledgeV2 } from "../../knowledge/internetKnowledgeV2Engine.js";
import { buildArchitectureKnowledgeV2 } from "../../knowledge/architectureKnowledgeV2Engine.js";
import { buildArchitectureKnowledge as buildArchitectureKnowledgeV18, buildConceptGraph as buildConceptGraphV18, buildDependencyKnowledge as buildDependencyKnowledgeV18, buildDocumentationKnowledge as buildDocumentationKnowledgeV18, buildRepositoryKnowledge as buildRepositoryKnowledgeV18, buildSemanticIdentity, resolveEntities as resolveEntitiesV18 } from "../../knowledge/reconstruction/index.js";

export { buildArchitectureKnowledgeV18, buildArchitectureKnowledgeV2, buildConceptGraph, buildConceptGraphV18, buildDependencyKnowledgeV18, buildDependencyLineage, buildDocumentKnowledgeV2, buildDocumentationKnowledgeV18, buildExecutionFlow, buildFrameworkRelationships, buildInternetKnowledgeV2, buildKnowledgeRelationshipsV2, buildRepositoryKnowledge, buildRepositoryKnowledgeV18, buildRepositoryKnowledgeV2, buildSemanticGraph, buildSemanticIdentity, buildServiceRelationships, clusterSemanticGraph, reasonOverSemanticGraph, resolveEntities, resolveEntitiesV18 };
