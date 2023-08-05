![lint status](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/lint.yml/badge.svg) ![release status](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/release.yml/badge.svg) ![tests status](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/tests.yml/badge.svg) ![docs status](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/deploy_docs.yml/badge.svg)


# BlueQubit Python SDK

## Usage

### Interface with the BlueQubit server

### Circuit serialization

You can decode a quantum circuit of Braket/Cirq/Qiskit to/from JSON string.

```python
import bluequbit.circuit_serialization as circuit_serialization

# Example with Cirq circuit
encoded_cirq = circuit_serialization.encode_circuit(qc_cirq)
decoded_cirq = circuit_serialization.decode_circuit(encoded_cirq)
```
