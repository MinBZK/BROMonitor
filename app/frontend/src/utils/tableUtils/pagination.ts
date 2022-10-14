export function getPaginationByField(field: string, descending = true) {
  return {
    page: 1,
    rowsPerPage: 10,
    sortBy: field,
    descending: descending,
  };
}
