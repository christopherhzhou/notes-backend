# notes-backend

Responses are structured this way:
{
    code: '<a string that represents the success/failure of a call>'
    detail: '<always included if code represents an error>'
    data: [] or {} // empty if statusCode represents an error/failure
    