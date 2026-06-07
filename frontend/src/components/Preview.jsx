import React, { useState } from "react";
import { Document, Page } from "react-pdf";

export default function Preview() {
  const [file, setFile] = useState(null);

  return (
    <div>
      <h3>Resume Preview</h3>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {file && (
        <Document file={file}>
          <Page pageNumber={1} />
        </Document>
      )}
    </div>
  );
}