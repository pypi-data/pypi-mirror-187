import React from "react";
import { Input, AutocompleteDropdown } from "react-invenio-forms";
import _capitalize from "lodash/capitalize";
import PropTypes from "prop-types";
import { Form, Segment, Header } from "semantic-ui-react";
import { AdminArrayField } from "./array";
import _isEmpty from "lodash/isEmpty";
import { sortFields } from "../components/utils";

const fieldsMap = {
  string: Input,
  integer: Input,
  uuid: Input,
  datetime: Input,
};

const generateFieldProps = (
  fieldName,
  fieldSchema,
  parentField,
  isCreate,
  formFieldConfig
) => {
  let currentFieldName;

  const fieldLabel = formFieldConfig?.text || fieldSchema?.title || fieldName;
  const placeholder =
    formFieldConfig?.placeholder || fieldSchema?.metadata?.placeholder;

  if (parentField) {
    currentFieldName = `${parentField}.${fieldName}`;
  } else {
    currentFieldName = fieldName;
  }

  const htmlDescription = (
    <div
      dangerouslySetInnerHTML={{
        __html: formFieldConfig?.description || fieldSchema?.metadata?.description,
      }}
    />
  );

  return {
    fieldPath: currentFieldName,
    key: currentFieldName,
    label: _capitalize(fieldLabel),
    description: htmlDescription,
    required: fieldSchema.required,
    disabled: fieldSchema.readOnly || (fieldSchema.createOnly && !isCreate),
    placeholder,
  };
};

const mapFormFields = (obj, parentField, isCreate, formFieldsConfig, dropDumpOnly) => {
  if (!obj) {
    return null;
  }

  const sortedFields = sortFields(obj);

  const elements = Object.entries(sortedFields).map(([fieldName, fieldSchema]) => {
    if (fieldSchema.readOnly && dropDumpOnly) {
      return null;
    }

    const fieldProps = generateFieldProps(
      fieldName,
      fieldSchema,
      parentField,
      isCreate,
      formFieldsConfig[fieldName]
    );

    const showField =
      _isEmpty(formFieldsConfig) ||
      Object.prototype.hasOwnProperty.call(formFieldsConfig, fieldProps.fieldPath);

    if (!showField) {
      return null;
    }

    if (fieldSchema.type === "array") {
      return (
        <AdminArrayField
          key={fieldProps.fieldPath}
          fieldSchema={fieldSchema}
          isCreate={isCreate}
          mapFormFields={mapFormFields}
          formFields={formFieldsConfig}
          {...fieldProps}
        />
      );
    }

    if (fieldSchema.type === "vocabulary") {
      return (
        <AutocompleteDropdown
          key={fieldProps.fieldPath}
          required={fieldSchema.required}
          autocompleteFrom={`/api/vocabularies/${fieldSchema.metadata.type}`}
          {...fieldProps}
        />
      );
    }

    if (fieldSchema.type === "object") {
      // nested fields
      return (
        <React.Fragment key={fieldProps.fieldPath}>
          <Header attached="top" as="h5">
            {fieldProps.label}
          </Header>
          <Segment attached="bottom">
            <Form.Group grouped>
              {mapFormFields(
                fieldSchema.properties,
                fieldProps.fieldPath,
                isCreate,
                formFieldsConfig
              )}
            </Form.Group>
          </Segment>
        </React.Fragment>
      );
    }

    const Element = fieldsMap[fieldSchema.type];
    return <Element {...fieldProps} key={fieldProps.fieldPath} />;
  });

  return elements;
};

export const GenerateForm = ({ jsonSchema, create, formFields, dropDumpOnly }) => {
  const properties = jsonSchema;
  return <>{mapFormFields(properties, undefined, create, formFields, dropDumpOnly)}</>;
};

GenerateForm.propTypes = {
  jsonSchema: PropTypes.object.isRequired,
  create: PropTypes.bool,
  formFields: PropTypes.object,
  dropDumpOnly: PropTypes.bool,
};

GenerateForm.defaultProps = {
  create: false,
  formFields: undefined,
  dropDumpOnly: false,
};
