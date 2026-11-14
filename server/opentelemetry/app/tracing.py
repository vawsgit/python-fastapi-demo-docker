"""
This file contains all the required libraries to implement Open Telemetry with Fast API
"""

import os

# Add imports for OTel components into the application
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Import the AWS X-Ray for OTel Python IDs Generator into the application.
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator

# Instrumentation Packages
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor  # noqa: F401
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # noqa: F401

otlp_exporter = OTLPSpanExporter(
    endpoint=f"http://{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}"
)
# Processes traces in batches as opposed to immediately one after the other
span_processor = BatchSpanProcessor(otlp_exporter)
# Configures the Global Tracer Provider
trace.set_tracer_provider(
    TracerProvider(
        active_span_processor=span_processor, id_generator=AwsXRayIdGenerator()
    )
)
