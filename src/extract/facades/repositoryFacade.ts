/**
 * Converted from Python: core/extract/facades/repository_facade.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildDistributedGraph } from "../../repository/distributedGraphEngine.js";
import { reconstructDomainModel } from "../../repository/domainReconstructionEngine.js";
import { inferEventTopology } from "../../repository/eventTopologyEngine.js";
import { mapInfrastructure } from "../../repository/infraTopologyEngine.js";
import { inferOwnership } from "../../repository/ownershipInferenceEngine.js";
import { inferRuntimeTopology } from "../../repository/runtimeTopologyEngine.js";
import { inferServiceBoundaries } from "../../repository/serviceBoundaryEngine.js";
import { buildDependencyLineage as buildRepoDependencyLineageV18, buildDeploymentGraph, buildEventGraph, buildRuntimeGraph, classifyArchitecture as classifyArchitectureV18, inferOwnershipDomains, reconstructMonorepo as reconstructMonorepoV18, reconstructTopology } from "../../repository/reconstruction/index.js";
import { extractRepositoryAst } from "../../repository/intelligence/repositoryAstEngine.js";
import { buildSymbolGraph } from "../../repository/intelligence/symbolGraphEngine.js";
import { buildCallGraph } from "../../repository/intelligence/callGraphEngine.js";
import { detectFrameworks } from "../../repository/intelligence/frameworkDetectionEngine.js";
import { detectLanguages } from "../../repository/intelligence/languageDetectionEngine.js";
import { reconstructArchitecture } from "../../repository/intelligence/architectureReconstructionEngine.js";
import { extractApiContract } from "../../repository/intelligence/apiContractEngine.js";
import { detectBuildSystems } from "../../repository/intelligence/buildSystemEngine.js";
import { detectLocks } from "../../repository/intelligence/packageLockEngine.js";
import { summarizeRepository } from "../../repository/intelligence/repositorySummaryEngine.js";
import { traverseRepo } from "../../repository/recursive/repoTraversalEngine.js";
import { detectMonorepo } from "../../repository/recursive/monorepoEngine.js";
import { extractCiCd } from "../../repository/recursive/ciCdEngine.js";
import { buildSemanticCallGraph, buildSemanticImportGraph, buildSemanticRepositoryGraph, detectSemanticFrameworks, detectSemanticRuntime, extractSemanticAst, extractSemanticDependencies, inferSemanticBuildGraph, inferSemanticServices, reconstructSemanticApi, reconstructSemanticArchitecture, resolveSemanticSymbols } from "../../repository/semantic/index.js";
import { extractSemanticRepository } from "../../repository/semantic/semanticRepositoryEngine.js";

export { buildCallGraph, buildDeploymentGraph, buildDistributedGraph, buildEventGraph, buildRepoDependencyLineageV18, buildRuntimeGraph, buildSemanticCallGraph, buildSemanticImportGraph, buildSemanticRepositoryGraph, buildSymbolGraph, classifyArchitectureV18, detectBuildSystems, detectFrameworks, detectLanguages, detectLocks, detectMonorepo, detectSemanticFrameworks, detectSemanticRuntime, extractApiContract, extractCiCd, extractRepositoryAst, extractSemanticAst, extractSemanticDependencies, extractSemanticRepository, inferEventTopology, inferOwnership, inferOwnershipDomains, inferRuntimeTopology, inferSemanticBuildGraph, inferSemanticServices, inferServiceBoundaries, mapInfrastructure, reconstructArchitecture, reconstructDomainModel, reconstructMonorepoV18, reconstructSemanticApi, reconstructSemanticArchitecture, reconstructTopology, resolveSemanticSymbols, summarizeRepository, traverseRepo };
