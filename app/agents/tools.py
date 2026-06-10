from app.services.trace_service import (
    TraceService,
)

from app.services.explain_service import (
    ExplainService,
)

from app.services.security_review import (
    SecurityReviewService,
)

from app.services.rag_service import (
    RAGService,
)
from app.services.architecture_review import (
    ArchitectureReviewService,
)


trace_tool = TraceService()

explain_tool = ExplainService()

security_tool = SecurityReviewService()

rag_tool = RAGService()

architecture_tool = ArchitectureReviewService()

from app.services.scalability_review import ScalabilityReviewService

scalability_tool = ScalabilityReviewService()