import "./ScoreForm.css";

import {inject, observer} from "mobx-react";
import PropTypes from "prop-types";
import React, {Component} from "react";
import ScoreIcon from "riskofbias/robTable/components/ScoreIcon";
import QuillTextInput from "shared/components/QuillTextInput";
import SelectInput from "shared/components/SelectInput";
import Spacer from "shared/components/Spacer";
import TextInput from "shared/components/TextInput";
import h from "shared/utils/helpers";

import {hideScore} from "../constants";
import ScoreOverrideForm from "./ScoreOverrideForm";

class ScoreInput extends Component {
    constructor(props) {
        super(props);
        this.scoreId = `${h.randomString()}-score`;
    }
    componentDidMount() {
        // special-case if current value doesn't exist in list of valid values;
        // change the value to default (edge-case where response choices change)
        const {choices, value, defaultValue, handleChange} = this.props;
        if (!choices.map(c => c.id).includes(value)) {
            handleChange(defaultValue);
        }
    }
    render() {
        const {choices, value, handleChange, errors} = this.props;
        return (
            <>
                <SelectInput
                    id={this.scoreId}
                    label="Judgment"
                    choices={choices}
                    multiple={false}
                    value={value}
                    handleSelect={handleChange}
                    errors={errors}
                />
                <ScoreIcon score={value} />
            </>
        );
    }
}
ScoreInput.propTypes = {
    choices: PropTypes.arrayOf(PropTypes.object),
    value: PropTypes.number.isRequired,
    handleChange: PropTypes.func.isRequired,
    defaultValue: PropTypes.number.isRequired,
    errors: PropTypes.array,
};

@inject("store")
@observer
class ScoreForm extends Component {
    render() {
        let {score, store} = this.props,
            scoreChoices = store.metrics[score.metric_id].response_values.map(c => {
                return {id: c, label: store.settings.score_metadata.choices[c]};
            }),
            showScoreInput = !hideScore(score.score),
            defaultScoreChoice = store.metrics[score.metric_id].default_response,
            editableMetricHasOverrides = store.editableMetricHasOverrides(score.metric_id),
            direction_choices = Object.entries(store.settings.score_metadata.bias_direction).map(
                kv => {
                    return {id: kv[0], label: kv[1]};
                }
            ),
            showOverrideCreate = score.is_default === true,
            isOverride = score.is_default === false,
            errorClass = Object.keys(score.errors).length > 0 ? "border border-danger " : "";

        return (
            <>
                {isOverride ? <Spacer borderStyle="4px dashed #323a45" /> : null}
                <div className={`score-form container-fluid ${errorClass}`}>
                    <div className="row mt-3">
                        <div className="col-md-3">
                            {editableMetricHasOverrides ? (
                                <TextInput
                                    id={`${score.id}-label`}
                                    label="Label"
                                    name={`label-id-${score.id}`}
                                    onChange={e => {
                                        store.updateScoreState(score, "label", e.target.value);
                                    }}
                                    value={score.label}
                                />
                            ) : null}
                        </div>
                        <div className="col-md-9">
                            {showOverrideCreate ? (
                                <button
                                    className="btn btn-primary float-right"
                                    type="button"
                                    onClick={() => {
                                        store.createScoreOverride({
                                            metric: score.metric_id,
                                            riskofbias: score.riskofbias_id,
                                        });
                                    }}>
                                    <i className="fa fa-plus"></i>&nbsp;Create new override
                                </button>
                            ) : null}

                            {isOverride ? (
                                <button
                                    className="btn btn-danger float-right"
                                    type="button"
                                    onClick={() => store.deleteScoreOverride(score.id)}>
                                    <i className="fa fa-trash"></i>&nbsp;Delete override
                                </button>
                            ) : null}

                            {editableMetricHasOverrides ? (
                                score.is_default ? (
                                    <b title="Unless otherwise specified, all content will use this value">
                                        <i className="fa fa-check-square-o" />
                                        &nbsp;Default judgment
                                    </b>
                                ) : (
                                    <b title="Only selected override content will use this value">
                                        <i className="fa fa-square-o" />
                                        &nbsp;Override judgment
                                    </b>
                                )
                            ) : null}
                        </div>
                    </div>
                    <div className="row">
                        {showScoreInput ? (
                            <div className="col-md-3">
                                <ScoreInput
                                    choices={scoreChoices}
                                    value={score.score}
                                    defaultValue={defaultScoreChoice}
                                    handleChange={value => {
                                        store.updateScoreState(score, "score", parseInt(value));
                                    }}
                                    errors={score.errors.score}
                                />
                                <SelectInput
                                    id={`${score.id}-direction`}
                                    label="Bias direction"
                                    choices={direction_choices}
                                    multiple={false}
                                    value={score.bias_direction}
                                    handleSelect={value => {
                                        store.updateScoreState(
                                            score,
                                            "bias_direction",
                                            parseInt(value)
                                        );
                                    }}
                                    errors={score.errors.bias_direction}
                                />
                            </div>
                        ) : null}
                        <div className="col-md-9">
                            <QuillTextInput
                                id={`${score.id}-notes`}
                                className="score-editor"
                                value={score.notes}
                                onChange={htmlContent => {
                                    store.updateScoreState(score, "notes", htmlContent);
                                }}
                                errors={score.errors.notes}
                            />
                        </div>
                    </div>
                    {score.is_default ? null : <ScoreOverrideForm score={score} />}
                </div>
            </>
        );
    }
}

ScoreForm.propTypes = {
    score: PropTypes.object.isRequired,
    store: PropTypes.object,
};

export {ScoreForm, ScoreInput};
