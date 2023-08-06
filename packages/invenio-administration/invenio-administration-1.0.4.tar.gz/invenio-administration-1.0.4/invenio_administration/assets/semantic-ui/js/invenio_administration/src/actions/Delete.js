import { DeleteModalTrigger } from "./DeleteModalTrigger";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { Popup } from "semantic-ui-react";
import { i18next } from "@translations/invenio_administration/i18next";
import _get from "lodash/get";
import Overridable from "react-overridable";

class DeleteCmp extends Component {
  render() {
    const {
      disabledMessage,
      disable,
      title,
      resourceName,
      successCallback,
      idKeyPath,
      resource,
    } = this.props;
    return (
      <Popup
        content={disabledMessage}
        disabled={!disable}
        trigger={
          <span>
            <DeleteModalTrigger
              title={title}
              resourceName={resourceName}
              resource={resource}
              successCallback={successCallback}
              idKeyPath={idKeyPath}
              disabled={disable(resource)}
              apiEndpoint={_get(resource, "links.self")}
              disabledDeleteMessage={disabledMessage}
            />
          </span>
        }
      />
    );
  }
}

DeleteCmp.propTypes = {
  disabledMessage: PropTypes.string,
  title: PropTypes.string.isRequired,
  resourceName: PropTypes.string.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string,
  disable: PropTypes.func,
  resource: PropTypes.object.isRequired,
};

DeleteCmp.defaultProps = {
  disabledMessage: i18next.t("Resource is not deletable."),
  idKeyPath: "pid",
  disable: () => false,
};

export default Overridable.component("InvenioAdministration.DeleteAction", DeleteCmp);
