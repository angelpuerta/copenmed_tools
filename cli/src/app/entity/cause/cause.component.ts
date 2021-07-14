import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Cause } from "src/app/models/graphs";


@Component({
    selector: 'copenmed-cause',
    templateUrl: './cause.component.html',
    styleUrls: ['./cause.component.scss']
})
export class CauseComponent{

    @Input()
    sourceLabel: string = '';
    @Input()
    causeLabel: string = '';
    @Input()
    cause!: Cause;
    @Output()
    unselectCause: EventEmitter<void> = new EventEmitter();

    get explanations(){
        return this.cause.paths;
    }

    get edges(){
        return this.cause.edges;
    }

    get nodes(){
        return this.cause.nodes;
    }

    unselect(){
        this.unselectCause.emit();
    }
    
}