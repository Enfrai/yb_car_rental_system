
interface _Response {
    code: string;
    message: string;
    detail: string;
    data: object;
}

export default class API {
    url: string;
    data: Object;
    onStart: Function;
    onError: Function;
    onSuccess: Function;
    
    constructor(url: string, data: object, onStart: Function, onError: Function, onSuccess: Function) {
        this.url = url;
        this.data = data;
        this.onStart = onStart;
        this.onError = onError;
        this.onSuccess = onSuccess;
    }
    
    async post() {
        try {
            this.onStart && this.onStart()
            const res = await fetch(this.url, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.data),
            });

            if (!res.ok) {
                this.onError && this.onError("-1", "post failed", `${res.status}`);
                return;
            }

            const resp: _Response = await res.json();

            console.log(`response data: ${JSON.stringify(resp)}`)

            if (resp.code == '0') {
                this.onSuccess && this.onSuccess(resp.data ?? {});
            } else {
                this.onError && this.onError(resp.code, resp.message, resp.detail);
            }
        } catch (err) {
            if (err instanceof Error) {
                this.onError && this.onError("-1", err.message, '')
            } else {
                this.onError && this.onError("-2", 'unknown error', '');
            }
        }
    }
}