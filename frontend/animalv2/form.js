import _ from "lodash";
import h from "shared/utils/helpers";

import $ from "$";

import startupEndpointForm from "../animal/EndpointForm";

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
	processMultipleShowHides = function(form, showHides) {
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

			console.log("SETUP ON", alwaysEl, contingentEls, otherVal);
            h.setupOtherShowHideRelationship(
                alwaysEl,
                contingentEls,
                otherVal
            );
        }
	},

	
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
        // we hide this in CSS - and now once it's set up, we show it. This way, you don't see
        // effect/subtype blink out of visibility; you just see everything appear, which is nicer.
        // (why opacity? If using display:none instead of opacity: 0 in the css, then the page
        // scrolls to the top. Rather than track that down, just use opacity 0->1 which doesn't
        // have the same issue...)
        $("form#aniv2-experiment-form").css("opacity", 1);
    },

    guidelineFormStartup = function (f) {
		console.log("FORM SETUP");
        let form = $(f);
        form.find("#id_name").focus();

            // form.find("select[name$='-composition_purity']"),
            // form.find("input[name$='-composition_purity_other']"),

        let showHides = [
            [
                "select[name$='-guideline_status']", [
                    "input[name$='-name']",
                    "input[name$='-number']",
                    "input[name$='-version_year']",
                    "textarea[name$='-deviations']",
                    "select[name$='-compliance']",
                ], "YS"
            ],
        ]

		processMultipleShowHides(form, showHides);
    },

    animalGroupFormStartup = function (f) {
		console.log("FORM SETUP");
        let form = $(f);
        form.find("#id_name").focus();

		h.setupOtherShowHideRelationship(
			form.find("select[name$='-generation']"),
			form.find("input[name$='-generation_remarks']"),
			"OT"
		);

		h.setupOtherShowHideRelationship(
			form.find("select[name$='-cohort_type']"),
			form.find("input[name$='-cohort_type_remarks']"),
			"OTH"
		);
    },

    husbandryFormStartup = function (f) {
        let form = $(f);
        form.find("#id_name").focus();

        let showHides = [
            [ "select[name$='-animal_randomization']", "input[name$='-animal_randomization_remarks']", ["YES","OTH"] ],
            [ "select[name$='-cage_material']", "input[name$='-cage_material_remarks']", "OTH" ],
            [ "select[name$='-bedding_material']", "input[name$='-bedding_material_remarks']", "OTH" ],
            [ "select[name$='-enrichment_material']", "input[name$='-enrichment_material_remarks']", "OTH" ],
            [ "select[name$='-water_bottle_material']", "input[name$='-water_bottle_material_remarks']", "OTH" ],
            [ "select[name$='-animal_identification']", "input[name$='-animal_identification_remarks']", "OTH" ],
            [ "select[name$='-water']", "input[name$='-water_remarks']", "OTH" ],
        ]

		processMultipleShowHides(form, showHides);
    },

    treatmentFormStartup = function (f) {
        let form = $(f);
        form.find("#id_name").focus();

        let showHides = [
            [ "select[name$='-route_of_exposure']", "input[name$='-route_of_exposure_remarks']", "OTH" ],
            [ "select[name$='-exposure_method']", "input[name$='-exposure_method_remarks']", "OTHER" ],
        ]

		processMultipleShowHides(form, showHides);
    },

    doseGroupFormStartup = function (f) {
        let form = $(f);
        form.find("#id_name").focus();

        let showHides = [
            [ "select[name$='-dose_group_type']", "input[name$='-dose_group_type_remarks']", "OTH" ],
            [ "select[name$='-dose_units']", "input[name$='-dose_units_remarks']", "OTHER" ],
        ]

		processMultipleShowHides(form, showHides);
    },

    dosePreparationFormStartup = function (f) {
        let form = $(f);
        form.find("#id_name").focus();

        let showHides = [
            [ "select[name$='-vehicle']", "input[name$='-vehicle_remarks']", "OTHER" ],
            [ "select[name$='-unit']", "input[name$='-unit_remarks']", "OTHER" ],
            [ "select[name$='-formulation_type']", "input[name$='-formulation_type_remarks']", "OTH" ],
            [ "select[name$='-solubility']", "input[name$='-solubility_remarks']", "SOL" ],
            [ "select[name$='-analytical_verification']", "input[name$='-analytical_verification_remarks']", "VER" ],
            [ "select[name$='-preparation_frequency']", "input[name$='-preparation_frequency_remarks']", "OTH" ],
            [ "select[name$='-preparation_method']", "input[name$='-preparation_method_remarks']", "OTH" ],
        ]

		processMultipleShowHides(form, showHides);
    },

	endpointFormStartup = function (f) {
		let form = $(f);

		console.log("ENDPOINT FORM STARTUP!!!");
		console.log("ENDPOINT FORM STARTUP!!!");
		console.log("ENDPOINT FORM STARTUP!!!");
		console.log("ENDPOINT FORM STARTUP!!!");
		console.log("ENDPOINT FORM STARTUP!!!");

		// EHV kickoff - start
		let config = JSON.parse(form.find("#hxCustomContext_animalv2endpoint").html());
		let vocabSettings = JSON.parse(config.vocabulary);

		console.log("READ IN", config, vocabSettings);
		
		startupEndpointForm(document.getElementById("vocabWidgets"), vocabSettings);

		// remove the effect/effect-subtype widgets; we don't use those on mechanistic right now
		setTimeout(function() {
			let ehvFields = ["name", "system", "organ", "effect", "effect_subtype"];
			for (let i = 0 ; i < ehvFields.length ; i++) {
				let ehvField = ehvFields[i];
				$("div[id^='div_id_endpoint-'][id$='-" + ehvField + "']").each(function() {
					// need to do two things actually:
					// 1. hide the default crispy UI; startupEndpointForm added other widgets/controls
					// 2. rename those UI things that startupEndpointForm  created; e.g.
					//    when editing endpoint #19, we'd want to rename the element "organ" that 
					//    startupEndpointForm created to "endpoint-19-organ".
					let ehvDiv = $(this);
					let actualPrefix = ehvDiv.attr("id").replace("div_id_", "").replace(ehvField, "");
					console.log("ACTUAL PREFIX == '" + actualPrefix + "'; EHV FIELD == '" + ehvField + "'");

					// thing 1
					$("input[type='hidden'][name='" + ehvField + "']").attr("name", actualPrefix + ehvField);
					$("input[type='hidden'][name='" + ehvField + "_term']").attr("name", actualPrefix + ehvField + "_term");

					// thing 2
					ehvDiv.remove();
					$("input[type='hidden'][id='id_" + actualPrefix + ehvField + "_term']").remove(); // the hidden widget(s) right before "remarks"...
				});
			}
			/*

			// hide effect/subtype -- the EHV system sort of assumes they are there, but we don't want
			// them in mechanistic...easiest route is just hide the widget, so they are alwauys blank in
			// the db. That way we don't have to muck with the existing term code
			$("div#vocabWidgets div.row div.col-md-3:eq(3)").remove();
			$("div#vocabWidgets div.row div.col-md-3:eq(2)").remove();

			// we hide this in CSS - and now once it's set up, we show it. This way, you don't see
			// effect/subtype blink out of visibility; you just see everything appear, which is nicer.
			// (why opacity? If using display:none instead of opacity: 0 in the css, then the page
			// scrolls to the top. Rather than track that down, just use opacity 0->1 which doesn't
			// have the same issue...)
			$("tr.mechanisticendpoint-edit-row").css("opacity", 1);
			*/
		}, 100);

		// EHV kickoff - end

		/*
		h.setupOtherShowHideRelationship(
			form.find("select[name$='-poa_process']"),
			form.find("input[name$='-poa_process_other']"),
			"OTHR"
		);

		h.setupOtherShowHideRelationship(
			form.find("select[name$='-poa_action']"),
			form.find("input[name$='-poa_action_other']"),
			"OTHR"
		);
		*/

		/*
		import("shared/components/JsonListWidget.js").then(function(module) {
			let widget = new module.default.widget_class();
			widget.initializeWidgetUi("poa");
			// widget.initializeAllWidgetUis();
		});
		*/
	},


	foo = null;





	/*
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
        } else if (e.target.querySelector(".form-guideline")) {
            guidelineFormStartup(e.target);
        } else if (e.target.querySelector(".form-animalgroup")) {
            animalGroupFormStartup(e.target);
        } else if (e.target.querySelector(".form-husbandry")) {
            husbandryFormStartup(e.target);
        } else if (e.target.querySelector(".form-treatment")) {
            treatmentFormStartup(e.target);
        } else if (e.target.querySelector(".form-dosegroup")) {
            doseGroupFormStartup(e.target);
        } else if (e.target.querySelector(".form-dosepreparation")) {
            dosePreparationFormStartup(e.target);
        } else if (e.target.querySelector(".form-animalv2endpoint")) {
            endpointFormStartup(e.target);
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
