# Caleon: Non-LLM Ethically-Grounded AI Stack

Caleon is a production-grade, seed-vault first AI architecture that implements philosophical reasoning through microservices. Built for ICS-V2-2025-10-18 compliance, it provides traceable, non-LLM decision making with immutable knowledge bases.

## Architecture

```
Seed Vault (Immutable Knowledge)
├── Epistemology: Kant, Locke, Hume, Spinoza
├── Logic: Deductive, Inductive, Intuitive, Monotonic/Non-monotonic
├── Ethics: Proverbs, Hedonic Reflex
├── Physics: Constants, Units & Measurements
└── Reference: Biology, Geography, History, Math, Physics, Psychology

Microservices (12-Factor Apps)
├── Cochlear Processor → Resonator Pyramid → Helix Services → Harmonizer → Phonatory Output
├── Each service mounts seed-vault read-only
├── Runtime data: Reflections, Glyphs, Audit logs
└── Ethics simulation via seed cross-referencing
```

## Quick Start

### Local Development
```bash
# Validate seed vault
make lint

# Run ethics simulation
make sim ACTION="lie to protect life"

# Start full stack
make up
```

### Production Deployment
```bash
# Install Helm chart
helm install caleon ./caleon-helm

# With monitoring & HA
helm install caleon ./caleon-helm \
  --set metrics.enabled=true \
  --set podDisruptionBudget.enabled=true
```

## Features

- ✅ **Seed-Vault First**: Immutable knowledge base with hash validation
- ✅ **Non-LLM**: Pure rule-based reasoning, no transformers
- ✅ **Ethics Traceable**: Every decision carries vault hash + glyph
- ✅ **ICS-V2-2025-10-18**: Versioned, checksummed, zero-trust
- ✅ **Production Ready**: RBAC, NetworkPolicy, PodDisruptionBudget
- ✅ **GitOps Ready**: Full Helm chart with optional CSI immutable mounts

## Project Structure

```
caleon/
├── bin/                      # CLI entry-points
├── services/                 # 12-factor micro-services
├── seed_vault/               # Single source of truth
├── runtime/                  # Mutable data (logs, reflections)
├── schemas/                  # JSON-Schema for seed validation
├── scripts/                  # Python utilities
├── caleon-helm/              # Production Helm chart
├── Dockerfile                # Base image
├── docker-compose.yml        # Local development
└── Makefile                  # Development tasks
```

## Scripts

- `seed-linter.py`: Validate vault integrity
- `ethics-simulator.py`: Dry-run decisions through seeds
- `package-vault.py`: Build .svbin binary packages
- `caleon_cipher.py`: Quantum-safe file encryption (ChaCha20 + Keccak + Module-LWE KEM)

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add seed files to appropriate vault
4. Run `make lint` to validate
5. Submit PR with ethics impact assessment

## Security

- All images must be signed (Gatekeeper policy available)
- Seed vault is immutable and checksummed
- Network policies restrict inter-service communication
- RBAC limits ConfigMap access to runtime namespace