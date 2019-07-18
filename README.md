# Canotic API Client
Use this library to interact with Canotic API

## Build
```
python setup.py bdist_wheel
```
## Install
```
pip install --upgrade dist/canotic_api_client-0.0.1-py3-none-any.whl
```
## Usage

### CLI
```
canotic-api-cli --help
```

### Python example
```python
import canotic as ca

client = ca.Client("CANOTIC_API_KEY")

client.create_job(api_id="APP_ID:",
		callback_url='http://www.example.com/callback',
		inputs=[{"data_url":"http://i.imgur.com/XOJbalC.jpg"}]
)

```
