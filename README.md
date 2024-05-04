* INSTALLATION

- Tạo venv:

```
python -m venv rd_venv
```
- Activate venv:
```
cd rd_venv/Scripts
.\activate
```
- Tạo folder src :

```
cd ../
mkdir src
cd src
```
- Clone git và pull git: Fork git này về git của bạn sau đó :
    ```
    git clone https://github.com/{tên-git-của-bạn}/openai-api-example
    ```
- Cài các thư viện:
    ```
    python -m pip install -r requirements.txt
    ```
- Cài env
    ```
    cp .env.example .env
    ```
    Và thay đổi API Key bằng API Key của bạn
