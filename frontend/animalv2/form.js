import _ from "lodash";
import h from "shared/utils/helpers";

import $ from "$";

const /*cloneSubformRow = function (lastRow, totalFormField) {
        // adapted from https://stackoverflow.com/questions/501719/
        const newElement = lastRow.clone(true);
        let total = totalFormField.val();
        newElement.find(":input").each(function () {
            const name = $(this)
                    .attr("name")
                    .replace(`-${total - 1}-`, `-${total}-`),
                id = `id_${name}`;
            $(this).attr({name, id}).val("").removeAttr("checked");
        });
        newElement.find("label").each(function () {
            var newFor = $(this)
                .attr("for")
                .replace(`-${total - 1}-`, `-${total}-`);
            $(this).attr("for", newFor);
        });
        total++;
        totalFormField.val(total);
        lastRow.after(newElement);

        // TODO - some DOM elements (the outer td and some of the help labeling) are wrong; fix
        newElement.find("td, small").each(function () {
            const loopEl = $(this),
                incorrectId = loopEl.attr("id");
            loopEl.attr("id", incorrectId.replace(`-${total - 2}-`, `-${total - 1}-`));
        });
    },*/
    experimentFormStartup = function (f) {
        let form = $(f);
        form.find("#id_name").focus();
        console.log("EXP FORM STARTUP!!!!!\n");

		h.setupOtherShowHideRelationship(
			form.find("select#id_experiment_type"),
			form.find("input#id_experiment_type_other"),
			"OTH"
		);

		h.setupOtherShowHideRelationship(
			form.find("select#id_experiment_type"),
			form.find("input#id_dev_or_repro_toxicity_types_0"), // any checkbox will do...
			"DTR"
		);
		/*
        let showHides = [
            [ "select#id_study_type", "input#id_study_type_other", "OTH" ],
            [ "select#id_route_of_administration", "input#id_route_of_administration_other", "OTH" ],
            [
                "select#id_has_guideline", [
                    "input#id_guideline_name",
                    "input#id_guideline_number",
                    "input#id_guideline_version_year",
                    "input#id_guideline_deviations",
                ], "YS"
            ],
        ]

        for (let i = 0 ; i < showHides.length ; i++) {
            let showHide = showHides[i];
            let alwaysSelector = showHide[0];
            let contingentSelectors = showHide[1];
            if (!Array.isArray(contingentSelectors)) {
                contingentSelectors = [contingentSelectors];
            }
            let otherVal = showHide[2];

            let alwaysEl = form.find(alwaysSelector);
            let contingentEls = contingentSelectors.map((x) => form.find(x));

            h.setupOtherShowHideRelationship(
                alwaysEl,
                contingentEls,
                otherVal
            );
        }
		*/

        // we hide this in CSS - and now once it's set up, we show it. This way, you don't see
        // effect/subtype blink out of visibility; you just see everything appear, which is nicer.
        // (why opacity? If using display:none instead of opacity: 0 in the css, then the page
        // scrolls to the top. Rather than track that down, just use opacity 0->1 which doesn't
        // have the same issue...)
        $("form#aniv2-experiment-form").css("opacity", 1);
    };/*
    chemicalFormStartup = function (f) {
        let form = $(f);

        h.setupOtherShowHideRelationship(
            form.find("select[name$='-composition_purity']"),
            form.find("input[name$='-composition_purity_other']"),
            "OTH"
        );
	},
    animalGroupFormStartup = function (form) {
        // TODO - fix - name is `animalgroup-1-species`
        let onSpeciesChange = function (_e, onStrainUpdateComplete) {
            // only show proper strains for a given species
            let selected = $("#id_strain option:selected").val();
            let update_strain_opts = function (d) {
                var opts = _.map(d, function (v, _i) {
                    return `<option value="${v.id}">${v.name}</option>`;
                }).join("");

                $("#id_strain").html(opts);
                $(`#id_strain option[value="${selected}"]`).prop("selected", true);

                if (onStrainUpdateComplete !== undefined) {
                    onStrainUpdateComplete();
                }
            };
            $.get("/assessment/api/strain", {species: $("#id_species").val()}, update_strain_opts);
        };
        $(form).find("#id_species").change(onSpeciesChange).trigger("change");

        // refresh species after "Add new strain" popup closes. Wait half a second
        // to give the addition, if any, time to register.
        $("a[title='Create strain']").on(
            window.app.HAWCUtils.HAWC_NEW_WINDOW_POPUP_CLOSING,
            function (_e) {
                setTimeout(function () {
                    let numStrainsBefore = $("#id_strain option").length;

                    // reload the species
                    onSpeciesChange(null, function () {
                        let strains = $("#id_strain option");

                        if (strains.length > numStrainsBefore) {
                            // a new one was added; let's select it.
                            let highestId = -1;
                            strains.each(function () {
                                highestId = Math.max(Number($(this).val()), highestId);
                            });

                            $("#id_strain").val(highestId);
                        }
                    });
                }, 500);
            }
        );
    },
    dataExtractionFormStartup = function (form) {
        // TODO fix - names are dataextraction-1-is_qualitative_only
        let onQualitativeChange = function () {
            let isQualOnly = $(form).find("#id_is_qualitative_only").is(":checked");

            let quantitativeFields = [
                "data_location",
                "dataset_type",
                "variance_type",
                "statistical_method",
                "statistical_power",
                "method_to_control_for_litter_effects",
                "values_estimated",
                "response_units",
                "dose_response_observations",
                "result_details",
            ];

            quantitativeFields.forEach(function (fieldName) {
                // ok to just hide values; the server will validate
                let parentDiv = $(`#id_${fieldName}`).parents("div.form-group");
                if (isQualOnly) {
                    parentDiv.addClass("hidden");
                } else {
                    parentDiv.removeClass("hidden");
                }
            });
        };

        $(form).find("#id_is_qualitative_only").change(onQualitativeChange).trigger("change");
    },
    formsetSetup = function (form, prefixes) {
        if (!Array.isArray(prefixes)) {
            prefixes = [prefixes];
        }

        $(form)
            .find("button.add-subobject")
            .each(function (index, _element) {
                $(this).click(function () {
                    const formPrefix = prefixes[index],
                        parentWrapper = $(this).parent("div.formset_wrapper"),
                        lastRow = parentWrapper.find("tr:last"),
                        totalFormField = parentWrapper.find(
                            `input[name="${formPrefix}-TOTAL_FORMS"]`
                        );
                    cloneSubformRow(lastRow, totalFormField);
                });
            });
    };*/

export default document => {
    console.log("in aniv2 form.js formStartup...if UI js not firing, troubleshoot here");

    document.body.addEventListener("htmx:load", e => {
		console.log("HTMX LOAD");
        if (e.target.querySelector(".form-experiment")) {
            // ENTRY SCENARIO 2/2: during experiment update...
            experimentFormStartup(e.target);
		} /*else if (e.target.querySelector(".form-chemical")) {
            // ENTRY SCENARIO 2/2: during experiment update...
            chemicalFormStartup(e.target);
        } else if (e.target.querySelector(".form-animalgroup")) {
            animalGroupFormStartup(e.target);
        } else if (e.target.querySelector(".form-treatment")) {
            formsetSetup(e.target, "dosegroupform");
        } else if (e.target.querySelector(".form-dataextraction")) {
            dataExtractionFormStartup(e.target);
            formsetSetup(e.target, ["groupleveldataform", "animalleveldataform"]);
        }*/
    });

    $(document).ready(function () {
        if (false && $("form#form-mech-chemical").length == 1) {
			// chemical only via htmx
            chemicalFormStartup("form#form-mech-chemical");
        } else if ($("form legend").html() == "Create new experiment") {
            // ENTRY SCENARIO 1/2: during experiment create...
            experimentFormStartup($("form legend").parent("form"));
        }
    });
};
