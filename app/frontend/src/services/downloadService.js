import { exportFile } from "quasar";
import * as stringify from "csv-stringify";

// Some fields have a formatting function before being shown to the user
// This helper method applies the formatting function to the output data.
function applyFormattingFunction(data, column) {
  if (typeof column.field == "function") {
    data.forEach((d) => {
      d[column.name] = column.format(d[column.name]);
    });
  } else {
    data.forEach((d) => {
      d[column.field] = column.format(d[column.field]);
    });
  }
}

// Some fields in the column definitions are lambda functions.
// This helper method replaces the value in the outputdata by applying that function
// Prevents stringify from failing on a function as a key value
function applyFieldFunctions(data, columns) {
  const outputData = data.map((d) => JSON.parse(JSON.stringify(d))); // Deep copy
  for (let i = 0; i < columns.length; i++) {
    const c = columns[i];
    if (c.field) {
      if (typeof c.field == "function") {
        outputData.forEach((d) => {
          d[c.name] = c.field(d);
        });
      }
      if (c.format) {
        applyFormattingFunction(outputData, c);
      }
    }
  }
  return outputData;
}

export function downloadTable(
  data,
  columns,
  fileName = "table-export",
  delimiter = ";"
) {
  const outputData = applyFieldFunctions(data, columns);
  stringify(
    outputData,
    {
      columns: columns
        .filter((c) => c.field)
        .map((c) => {
          if (typeof c.field == "function") {
            return { key: c.name, header: c.label };
          } else {
            return { key: c.field, header: c.label };
          }
        }),
      delimiter: delimiter,
      header: true,
      quoted: true,
    },
    function(err, output) {
      if (err) {
        alert("Er is iets fout gegaan bij het downloaden van de CSV!");
        return;
      }
      exportFile(`${fileName}.csv`, output, "text/csv");
    }
  );
}
