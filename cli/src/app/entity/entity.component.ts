import { Component } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { filter, map, mergeMap } from 'rxjs/operators';
import { Cause, Graph } from "../models/graphs";
import { RetrieveRelationshipService } from "../service/retrieve_relationship.service";


@Component({
    selector: 'copenmed-entity',
    templateUrl: './entity.component.html',
    styleUrls: ['./entity.component.scss']
})
export class Entity{

    graphs: Graph[] = [];
    sourceLabel: string = '';
    selectedCause: string = '';
   
    constructor(
        private route: ActivatedRoute,
        private relationshipService: RetrieveRelationshipService
      ) {
        this.route.params.pipe(
            filter((params) => ("entity" in params)),
            map((params)=> params["entity"]),
            mergeMap((entity) => this.relationshipService.getRelationships(entity))
        ).subscribe(
            (graphs)=> {
                this.graphs = graphs.graphs;
                this.sourceLabel = graphs.label;
            }
        );
       }
    
    getCauses():string[]{
        return this.graphs.map(graph => graph.graph.label);
    }

    selectCause(event:string) {
        this.selectedCause = event;
    }

    deselectCause(){
        this.selectedCause = '';
    }

    selectedCauseGraph(): Cause{
        const cause = this.graphs.find(graph => graph.graph.label ===  this.selectedCause);
        if(!cause){
            throw new Error("Cause not detected");
        }
        return cause.graph;
      }
      
}