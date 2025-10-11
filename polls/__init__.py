from ddtrace import tracer

# Span تجريبي للتأكد من عمل Datadog APM
with tracer.trace("startup.span", resource="startup"):
    print("Datadog tracer is running!")
